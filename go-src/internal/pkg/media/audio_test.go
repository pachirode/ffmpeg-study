package media

import (
	"context"
	"os"
	"testing"
	"time"
)

func TestAudioProcessor_Decode(t *testing.T) {
	inputPath := "../../../../assest/trailer.mkv"
	if _, err := os.Stat(inputPath); err != nil {
		if os.IsNotExist(err) {
			t.Fatal("Fatal file not exist")
		}
		t.Errorf("Error to stat file: %#V", err)
	}

	ap := &AudioProcessor{}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	ap.Decode(ctx, inputPath)
}

func TestAudioProcessor_TransCode(t *testing.T) {
	inputPath := "../../../../assest/trailer.mkv"
	if _, err := os.Stat(inputPath); err != nil {
		if os.IsNotExist(err) {
			t.Fatal("Fatal file not exist")
		}
		t.Errorf("Error to stat file: %#V", err)
	}

	ap := &AudioProcessor{}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	ap.Transcode(ctx, inputPath, "wav")
}
