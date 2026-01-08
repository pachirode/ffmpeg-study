package media

type MediaBiz interface {
	Audio() *audioBiz
}

type MediaCommon interface{}

type mediaBiz struct {
	audio *audioBiz
}

var _ MediaBiz = (*mediaBiz)(nil)

func NewMedia() *mediaBiz {
	return &mediaBiz{audio: (*audioBiz)(NewAudioProcessor())}
}

func (b *mediaBiz) Audio() *audioBiz {
	return b.audio
}
