package utils

import "fmt"

func GetTargetFormatArgs(format string) ([]string, error) {
	switch format {
	case "pcm":
		return []string{"-f", "s16le", "-ar", "44100", "-ac", "2"}, nil
	case "wav":
		return []string{"-ar", "44100", "-ac", "2"}, nil // WAV 默认使用 pcm_s16le
	case "mp3":
		return []string{"-ar", "44100", "-ac", "2", "-codec:a", "libmp3lame"}, nil
	case "aac":
		return []string{"-ar", "44100", "-ac", "2", "-codec:a", "aac"}, nil
	case "flac":
		return []string{"-ar", "44100", "-ac", "2", "-codec:a", "flac"}, nil
	default:
		return nil, fmt.Errorf("unsupported target format: %s", format)
	}
}
