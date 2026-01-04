package main

import (
	"os"

	"github.com/pachirode/ffmpeg-study/cmd/apiserver/app"
)

func main() {
	command := app.NewServerCommand()

	if err := command.Execute(); err != nil {
		os.Exit(1)
	}
}
