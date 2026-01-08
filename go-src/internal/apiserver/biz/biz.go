package biz

import (
	mediaV1 "github.com/pachirode/ffmpeg-study/internal/apiserver/v1/media"
)

type IBiz interface {
	Media() mediaV1.MediaBiz
}

type biz struct{}

var _ IBiz = (*biz)(nil)

func NewBiz() *biz {
	return &biz{}
}

func (b *biz) Media() mediaV1.MediaBiz {
	return mediaV1.NewMedia()
}
