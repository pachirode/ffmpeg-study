package grpc

import (
	"github.com/pachirode/ffmpeg-study/internal/apiserver/biz"
	apiv1 "github.com/pachirode/ffmpeg-study/pkg/api/apiserver/v1"
)

type Handler struct {
	apiv1.UnimplementedFFmpegAudioStreamServiceServer

	biz biz.IBiz
}

func NewHandler(biz biz.IBiz) *Handler {
	return &Handler{
		biz: biz,
	}
}
