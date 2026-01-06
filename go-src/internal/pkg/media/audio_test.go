package media

import (
	"context"
	"log"
	"os"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pachirode/ffmpeg-study/internal/pkg/utils"
)

var (
	id          string
	inputPath   = "../../../../assest/trailer.mkv"
	out         = "../../../../assest/tmp.mkv"
	ap          = &AudioProcessor{}
	ctx, cancel = context.WithTimeout(context.Background(), 50*time.Second)
)

func TestMain(m *testing.M) {
	log.Println("TestMain judge inputfile")
	if _, err := os.Stat(inputPath); err != nil {
		if os.IsNotExist(err) {
			log.Fatalln("Input file not found")
			os.Exit(-1)
		}
		log.Fatalf("Error stat file %v", err)
		os.Exit(-1)
	}
	id = uuid.NewString()
	defer cancel()
	log.Println("TestMain start cleanup loop")

	utils.StartCleanup(1 * time.Minute)
	defer utils.ShutdownCleanup()
	m.Run()
}

func TestAudioProcessor_Decode(t *testing.T) {
	ap.Decode(ctx, id, inputPath)
}

func TestAudioProcessor_TransCode(t *testing.T) {
	ap.Transcode(ctx, id, inputPath, "wav")
}

func TestAudioProcessor_Clip(t *testing.T) {
	ap.Clip(ctx, id, inputPath, 5*time.Second, 2*time.Second)
}

func TestAudioProcessor_SpeedChange(t *testing.T) {
	ap.SpeedChange(ctx, id, inputPath, 5)
}

func TestAudioProcessor_SetVolume(t *testing.T) {
	ap.SetVolume(ctx, uuid.NewString(), inputPath, 1.5)
}

func TestAudioProcessor_Output(t *testing.T) {
	ap.Output(ctx, id, out)
}
