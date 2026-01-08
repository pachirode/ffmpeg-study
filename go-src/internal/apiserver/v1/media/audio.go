package media

import (
	"sync"

	mediaV1 "github.com/pachirode/ffmpeg-study/internal/pkg/media"
)

type AudioBiz interface {
	MediaCommon
}

type audioBiz struct{}

var (
	_              AudioBiz = (*audioBiz)(nil)
	audioOnce      sync.Once
	audioProcessor *mediaV1.AudioProcessor
)

func NewAudioProcessor() *mediaV1.AudioProcessor {
	audioOnce.Do(func() {
		audioProcessor = mediaV1.NewAudioProcessor()
	})
	return audioProcessor
}
