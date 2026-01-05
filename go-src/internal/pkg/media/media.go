package media

import (
	"context"
)

// MediaProcessor 定义音视频处理的公共方法
type MediaProcessor interface {
	// Decode 解码输入文件或流
	Decode(ctx context.Context, inputPath string) (string, error)

	// Transcode 转码到指定格式
	Transcode(ctx context.Context, inputPath, targetFormt string) (string, error)

	// Clip 裁剪指定时间段
	Clip(ctx context.Context, inputPath, outputPath string, startSeconds, durationSeconds float64) error

	// SpeedChange 调整播放速度
	SpeedChange(ctx context.Context, inputPath, outputPath string, speed float64) error

	// SetVolume 调整音量（音频专用，可视频实现为空）
	SetVolume(ctx context.Context, inputPath, outputPath string, volume float64) error

	// Output 输出到文件或管道
	Output(ctx context.Context, inputPath, outputPath string) error
}
