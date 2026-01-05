package media

import (
	"context"

	"github.com/pachirode/ffmpeg-study/internal/pkg/utils"
)

func GetFileInfo(ctx context.Context, inputPath string) (*utils.MediaInfo, error) {
	return utils.GetFileInfo(ctx, inputPath)
}
