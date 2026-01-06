package media

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/pachirode/pkg/log"

	"github.com/pachirode/ffmpeg-study/internal/pkg/utils"
)

type AudioProcessor struct{}

var (
	_          MediaProcessor = (*AudioProcessor)(nil)
	outputPath string
)

// Decode 统一转成 PCM 格式数据
func (p *AudioProcessor) Decode(ctx context.Context, id, inputPath string) (string, error) {
	outputPath, err := utils.RunffmpegTran(ctx, id, inputPath, "pcm")
	if err != nil {
		log.Fatalw("ffmpeg failed", "err", err)
	}

	info, _ := os.Stat(outputPath)
	if info.Size() == 0 {
		log.Fatalw("Failed to generate PCM data")
	}

	log.Infow("FFmpeg decode successfully", "size", info.Size(), "path", outputPath)

	return outputPath, nil
}

// Transcode 将其转换成为其他格式，直接转换失败，就是用 pcm 中转
func (p *AudioProcessor) Transcode(ctx context.Context, id, inputPath, targetFormat string) (string, error) {
	outputPath, err := utils.RunffmpegTran(ctx, id, inputPath, targetFormat)
	if err != nil {
		if targetFormat == "pcm" {
			return "", err
		}
		log.Fatalf("Failed to convert format %v, try convert to pcm first", targetFormat)
	} else {
		log.Infof("Transcode successfully", "path", outputPath)
		return outputPath, nil
	}

	pcmPath, err := p.Decode(ctx, "tmp", inputPath)
	if err != nil {
		return "", err
	}
	outputPath, err = utils.RunffmpegTran(ctx, id, pcmPath, targetFormat)
	if err != nil {
		return "", nil
	}

	log.Infof("Transcode successfully", "path", outputPath)

	return outputPath, err
}

// Clip  按照时长裁剪媒体文件
func (p *AudioProcessor) Clip(ctx context.Context, id, inputPath string, start, length time.Duration) (string, error) {
	outputPath, err := utils.Clip(ctx, id, inputPath, start, length)
	if err != nil {
		return "", nil
	}
	log.Infof("Clip successfully", "path", outputPath)

	return outputPath, err
}

// SpeedChange 设置媒体速度
func (p *AudioProcessor) SpeedChange(ctx context.Context, id, inputPath string, speed float64) (string, error) {
	if speed <= 0 {
		return "", fmt.Errorf("speed must be > 0")
	}
	outputPath, err := utils.SpeedChange(ctx, id, inputPath, speed)
	if err != nil {
		return "", nil
	}
	log.Infof("SpeedChange successfully", "path", outputPath)

	return outputPath, nil
}

// SetVolume 音量调整
func (p *AudioProcessor) SetVolume(ctx context.Context, id, inputPath string, volume float64) (string, error) {
	if volume <= 0 {
		return "", fmt.Errorf("volume must be > 0")
	}

	outputPath, err := utils.SetVolume(ctx, id, inputPath, volume)
	if err != nil {
		return "", err
	}
	log.Infof("SetVolume successfully", "path", outputPath)

	return outputPath, nil
}

// Output 将处理之后的音频文件写到指定路径
func (p *AudioProcessor) Output(ctx context.Context, id, outputPath string) error {
	return utils.Output(id, outputPath)
}
