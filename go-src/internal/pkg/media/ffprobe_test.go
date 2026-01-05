package media

import (
	"context"
	"os"
	"testing"
	"time"
)

func TestGetFileInfo(t *testing.T) {
	inputPath := "../../../../assest/trailer.mkv"
	if _, err := os.Stat(inputPath); err != nil {
		if os.IsNotExist(err) {
			t.Fatal("Fatal file not exist")
		}
		t.Errorf("Error to stat file: %#V", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	info, err := GetFileInfo(ctx, inputPath)
	if err != nil {
		t.Errorf("Error to get file info: %v", err)
	} else {
		t.Log("Get info successfully", "info", info)
	}
}
