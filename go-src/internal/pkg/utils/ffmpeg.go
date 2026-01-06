package utils

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
	"time"

	"github.com/pachirode/pkg/log"
)

func Runffmpeg(ctx context.Context, id, inputPath string, format string, args []string) (string, error) {
	tmp, err := os.CreateTemp("", fmt.Sprintf("ffmpeg_output_*.%s", format))
	if err != nil {
		return "", fmt.Errorf("create temp file failed: %w", err)
	}
	tmp.Close()
	RegisterTmp(id, tmp.Name())
	err = MarkInRunning(id)
	if err != nil {
		return "", nil
	}
	defer MarkReleased(id)

	finalArgs := []string{"-y", "-i", inputPath}
	finalArgs = append(finalArgs, args...)
	finalArgs = append(finalArgs, tmp.Name())

	var out bytes.Buffer
	cmd := exec.CommandContext(ctx, "ffmpeg", finalArgs...)
	cmd.Stderr = &out
	cmd.Stdout = &out

	if err := cmd.Run(); err != nil {
		if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) {
			log.Errorw(err, "Error to run ffmpeg command, killed by context", "path", tmp.Name())
			return "", fmt.Errorf("ffmpeg killed by context: %w", err)
		}
		log.Errorw(err, "Error to run ffmpeg command", "path", tmp.Name())
		return "", fmt.Errorf(
			"ffmpeg failed: %w",
			err,
		)
	}

	log.Debugw("FFmpeg command successfully", "output", out.String(), "path", tmp.Name())

	return tmp.Name(), nil
}

func RunffmpegTran(ctx context.Context, id, inputPath, format string) (string, error) {
	args, err := GetTargetFormatArgs(format)
	if err != nil {
		return "", err
	}

	return Runffmpeg(ctx, id, inputPath, format, args)
}

func Clip(ctx context.Context, id, inputPath string, start, length time.Duration) (string, error) {
	info, err := GetFileInfo(ctx, inputPath)
	if err != nil {
		return "", err
	}

	if info.Duration <= 0 {
		return "", fmt.Errorf("invalid media duration")
	}

	if start < 0 {
		start = 0
	}

	if start >= info.Duration {
		return "", fmt.Errorf(
			"clip start (%v) exceeds media duration (%v)",
			start, info.Duration,
		)
	}

	if length <= 0 {
		return "", fmt.Errorf("clip length must be positive")
	}

	if start+length > info.Duration {
		length = info.Duration - start
	}

	args := []string{
		"-ss", formatSeconds(start),
		"-t", formatSeconds(length),
		"-c", "copy",
	}

	return Runffmpeg(ctx, id, inputPath, info.FileExt, args)
}

func formatSeconds(d time.Duration) string {
	return fmt.Sprintf("%.3f", d.Seconds())
}

func SpeedChange(ctx context.Context, id, inputPath string, speed float64) (string, error) {
	info, err := GetFileInfo(ctx, inputPath)
	if err != nil {
		return "", err
	}

	// 构造音频 atempo 链，因为音频限制 0.5-2
	atempoFilters := []string{}
	remaining := speed
	for remaining > 2.0 {
		atempoFilters = append(atempoFilters, "atempo=2.0")
		remaining /= 2.0
	}
	for remaining < 0.5 {
		atempoFilters = append(atempoFilters, "atempo=0.5")
		remaining /= 0.5
	}
	atempoFilters = append(atempoFilters, fmt.Sprintf("atempo=%.6f", remaining))
	audioFilter := strings.Join(atempoFilters, ",")

	args := []string{
		"-filter_complex",
		fmt.Sprintf("[0:v]setpts=PTS/%.6f[v];[0:a]%s[a]", speed, audioFilter),
		"-map", "[v]",
		"-map", "[a]",
	}

	return Runffmpeg(ctx, id, inputPath, info.FileExt, args)
}

func SetVolume(ctx context.Context, id, inputPath string, volume float64) (string, error) {
	info, err := GetFileInfo(ctx, inputPath)
	if err != nil {
		return "", err
	}

	args := []string{
		"-filter_complex",
		fmt.Sprintf("[0:a]volume=%.6f[a]", volume),
		"-map", "0:v?", // 可选视频
		"-map", "[a]", // 音频映射
	}

	return Runffmpeg(ctx, id, inputPath, info.FileExt, args)
}

func Output(id, outputPath string) error {
	mu.Lock()
	meta, ok := tmpFiles[id]
	mu.Unlock()

	if !ok || meta == nil {
		return fmt.Errorf("tmp id %s not found", id)
	}

	src, err := os.Open(meta.Path)
	if err != nil {
		return fmt.Errorf("open tmp file failed: %w", err)
	}
	defer src.Close()

	dst, err := os.Create(outputPath)
	if err != nil {
		return fmt.Errorf("create output file failed: %w", err)
	}
	defer dst.Close()

	if _, err := io.Copy(dst, src); err != nil {
		return fmt.Errorf("copy content failed: %w", err)
	}

	log.Infow("Output successfully", "path", outputPath)
	return nil
}
