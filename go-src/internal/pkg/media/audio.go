package media

import (
	"context"
	"fmt"
	"os"
	"os/exec"

	"github.com/pachirode/pkg/log"

	"github.com/pachirode/ffmpeg-study/internal/pkg/utils"
)

type AudioProcessor struct{}

var _ MediaProcessor = (*AudioProcessor)(nil)

// Decode 统一转成 PCM 格式数据
func (p *AudioProcessor) Decode(ctx context.Context, inputPath string) (string, error) {
	outputPath, err := utils.Runffmpeg(ctx, inputPath, "pcm")
	if err != nil {
		log.Fatalw("ffmpeg failed", "err", err)
	}

	info, _ := os.Stat(outputPath)
	if info.Size() == 0 {
		log.Fatalw("Failed to generate PCM data")
	}

	log.Infow("FFmpeg decode successfully", "size", info.Size(), "path", outputPath)
	defer os.Remove(outputPath)

	return outputPath, nil
}

// Transcode 将其转换成为其他格式，直接转换失败，就是用 pcm 中转
func (p *AudioProcessor) Transcode(ctx context.Context, inputPath, targetFormat string) (string, error) {
	outputPath, err := utils.Runffmpeg(ctx, inputPath, targetFormat)
	if err != nil {
		if targetFormat == "pcm" {
			return "", err
		}
		log.Fatalf("Failed to convert format %v, try convert to pcm first", targetFormat)
	} else {
		log.Infof("Transcode successfully", "path", outputPath)
		return outputPath, nil
	}

	pcmPath, err := p.Decode(ctx, inputPath)
	if err != nil {
		return "", err
	}
	outputPath, err = utils.Runffmpeg(ctx, pcmPath, targetFormat)

	log.Infof("Transcode successfully", "path", outputPath)
	defer os.Remove(outputPath)
	return outputPath, err
}

func (p *AudioProcessor) Clip(ctx context.Context, inputPath, outputPath string, start, duration float64) error {
	cmd := exec.CommandContext(ctx, "ffmpeg",
		"-ss", fmt.Sprintf("%.2f", start),
		"-t", fmt.Sprintf("%.2f", duration),
		"-i", inputPath,
		outputPath,
	)
	return cmd.Run()
}

func (p *AudioProcessor) SpeedChange(ctx context.Context, inputPath, outputPath string, speed float64) error {
	cmd := exec.CommandContext(ctx, "ffmpeg",
		"-i", inputPath,
		"-filter:a", fmt.Sprintf("atempo=%.2f", speed),
		outputPath,
	)
	return cmd.Run()
}

func (p *AudioProcessor) SetVolume(ctx context.Context, inputPath, outputPath string, volume float64) error {
	cmd := exec.CommandContext(ctx, "ffmpeg",
		"-i", inputPath,
		"-filter:a", fmt.Sprintf("volume=%.2f", volume),
		outputPath,
	)
	return cmd.Run()
}

func (p *AudioProcessor) Output(ctx context.Context, inputPath, outputPath string) error {
	cmd := exec.CommandContext(ctx, "ffmpeg", "-i", inputPath, outputPath)
	return cmd.Run()
}
