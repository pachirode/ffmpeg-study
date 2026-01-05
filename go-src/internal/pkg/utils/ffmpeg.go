package utils

import (
	"bytes"
	"context"
	"fmt"
	"os"
	"os/exec"
)

func Runffmpeg(ctx context.Context, inputPath string, format string) (string, error) {
	args, err := GetTargetFormatArgs(format)
	if err != nil {
		return "", err
	}
	tmp, err := os.CreateTemp("", fmt.Sprintf("ffmpeg_output_*.%s", format))
	if err != nil {
		return "", fmt.Errorf("create temp file failed: %w", err)
	}
	tmp.Close()

	finalArgs := []string{"-y", "-i", inputPath}
	finalArgs = append(finalArgs, args...)
	finalArgs = append(finalArgs, tmp.Name())

	var stderr bytes.Buffer
	cmd := exec.CommandContext(ctx, "ffmpeg", finalArgs...)
	cmd.Stderr = &stderr

	if err := cmd.Run(); err != nil {
		os.Remove(tmp.Name())
		return "", fmt.Errorf(
			"ffmpeg failed: %w\nstderr:\n%s",
			err,
			stderr.String(),
		)
	}

	return tmp.Name(), nil
}
