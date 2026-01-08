package grpc

import (
	"io"
	"os/exec"
	"time"

	"google.golang.org/protobuf/types/known/timestamppb"

	apiV1 "github.com/pachirode/ffmpeg-study/pkg/api/apiserver/v1"
)

func (h *Handler) PullAudioStream(req *apiV1.StartAudioStreamRequest, stream apiV1.FFmpegAudioStreamService_PullAudioStreamServer) error {
	// 本地音频文件路径，可以改成 req.StreamId 对应的文件映射
	filePath := "C:\\Users\\RodePachi\\project\\ffpmeg-study\\assest\\trailer.mkv"

	// 使用 ffmpeg 将音频转成 PCM 数据流
	cmd := exec.Command(
		"ffmpeg",
		"-i", filePath, // 输入文件
		"-f", "s16le", // PCM 16bit little endian
		"-acodec", "pcm_s16le",
		"-ac", "2", // 双声道
		"-ar", "44100", // 采样率 44.1kHz
		"pipe:1", // 输出到 stdout
	)

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return err
	}

	if err := cmd.Start(); err != nil {
		return err
	}

	buf := make([]byte, 4096) // 每帧读取 4KB，可以按需调整
	for {
		n, err := stdout.Read(buf)
		if err != nil {
			if err == io.EOF {
				break
			}
			return err
		}

		packet := &apiV1.AudioPacket{
			Meta: &apiV1.AudioMeta{
				Codec:      "pcm_s16le",
				SampleRate: 44100,
				Channels:   2,
				StreamId:   req.StreamId,
				Pts:        timestamppb.Now(),
			},
			Data:      buf[:n],
			CreatedAt: timestamppb.Now(),
		}

		// 发送给客户端
		if err := stream.Send(packet); err != nil {
			return err
		}

		// 模拟实时播放节奏，可选
		time.Sleep(20 * time.Millisecond)
	}

	cmd.Wait()
	return nil
}
