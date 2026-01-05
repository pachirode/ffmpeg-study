package utils

import (
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"strconv"
)

// MediaInfo 用于表示文件的所有元数据
type MediaInfo struct {
	FormatName  string `json:"format_name"`
	CodecName   string `json:"codec_name"`
	Duration    string `json:"duration"`
	SampleRate  int    `json:"sample_rate,string"`
	Channels    int    `json:"channels"`
	BitRate     string `json:"bit_rate"`
	StreamCount int    `json:"stream_count"`
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

	out, err := cmd.Output()
	if err != nil {
		return nil, fmt.Errorf("ffprobe command failed: %v", err)
	}

	// 解析 JSON 输出
	var data struct {
		Format struct {
			FormatName string `json:"format_name"`
			Duration   string `json:"duration"`
			BitRate    string `json:"bit_rate"`
		} `json:"format"`
		Streams []struct {
			CodecName  string `json:"codec_name"`
			SampleRate string `json:"sample_rate"`
			Channels   int    `json:"channels"`
		} `json:"streams"`
	}

	if err := json.Unmarshal(out, &data); err != nil {
		return nil, fmt.Errorf("json decode failed: %v", err)
	}

	// 构建 MediaInfo 结构体
	mediaInfo := &MediaInfo{
		FormatName:  data.Format.FormatName,
		Duration:    data.Format.Duration,
		BitRate:     data.Format.BitRate,
		StreamCount: len(data.Streams),
	}

	if len(data.Streams) > 0 {
		mediaInfo.CodecName = data.Streams[0].CodecName
		if data.Streams[0].SampleRate != "" {
			mediaInfo.SampleRate, err = parseSampleRate(data.Streams[0].SampleRate)
			if err != nil {
				return nil, fmt.Errorf("Invalid sampling rate format: %v", err)
			}
		} else {
			mediaInfo.SampleRate = 0 // 采样率为空则置 0
		}
	}

	return mediaInfo, nil
}

// parseSampleRate 解析音频流中的采样率
func parseSampleRate(sampleRate string) (int, error) {
	if sampleRate == "" {
		return 0, nil
	}
	return strconv.Atoi(sampleRate)
}
