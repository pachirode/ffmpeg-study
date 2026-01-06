package utils

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
	"time"
)

// MediaInfo 用于表示文件的所有元数据
type MediaInfo struct {
	FormatName string        `json:"format_name"`
	Duration   time.Duration `json:"duration"`
	FileExt    string        `json:"file_ext"`

	HasVideo bool `json:"has_video"`
	HasAudio bool `json:"has_audio"`

	VideoCodec string `json:"video_codec"`
	AudioCodec string `json:"audio_codec"`

	Width      int `json:"width"`
	Height     int `json:"height"`
	SampleRate int `json:"sample_rate"`
}

type ffprobeResult struct {
	Streams []ffprobeStream `json:"streams"`
	Format  ffprobeFormat   `json:"format"`
}

type ffprobeStream struct {
	CodecType  string `json:"codec_type"`
	CodecName  string `json:"codec_name"`
	Width      int    `json:"width"`
	Height     int    `json:"height"`
	SampleRate string `json:"sample_rate"`
}

type ffprobeFormat struct {
	FormatName string `json:"format_name"`
	Duration   string `json:"duration"`
}

// GetFileInfo 获取音频/视频文件的所有信息
func GetFileInfo(ctx context.Context, filePath string) (*MediaInfo, error) {
	cmd := exec.CommandContext(ctx, "ffprobe",
		"-v", "error", // 静默模式，不输出日志
		"-show_format",  // 输出文件格式信息
		"-show_streams", // 输出流（音频/视频）信息
		"-of", "json",   // 输出格式为 JSON，方便解析
		filePath,
	)

	var stdout bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stdout

	if err := cmd.Run(); err != nil {
		return nil, fmt.Errorf(
			"ffprobe failed: %w, output: %s",
			err,
			stdout.String(),
		)
	}

	var probe ffprobeResult
	if err := json.Unmarshal(stdout.Bytes(), &probe); err != nil {
		return nil, err
	}

	info := &MediaInfo{
		FormatName: probe.Format.FormatName,
		FileExt:    getFileExt(filePath),
	}

	// 1. Duration（只从 format 读取）
	if probe.Format.Duration != "" {
		sec, err := strconv.ParseFloat(probe.Format.Duration, 64)
		if err != nil {
			return nil, fmt.Errorf(
				"invalid duration format: %s",
				probe.Format.Duration,
			)
		}
		info.Duration = time.Duration(sec * float64(time.Second))
	}

	// 2. Streams（codecType 完全由 ffprobe 决定）
	for _, s := range probe.Streams {
		switch s.CodecType {

		case "video":
			info.HasVideo = true
			info.VideoCodec = s.CodecName
			info.Width = s.Width
			info.Height = s.Height

		case "audio":
			info.HasAudio = true
			info.AudioCodec = s.CodecName

			if s.SampleRate != "" {
				sr, err := strconv.Atoi(s.SampleRate)
				if err != nil {
					return nil, fmt.Errorf(
						"invalid sampling rate: %s",
						s.SampleRate,
					)
				}
				info.SampleRate = sr
			}
		}
	}

	return info, nil
}

func getFileExt(path string) string {
	return strings.ToLower(filepath.Ext(path))[1:]
}
