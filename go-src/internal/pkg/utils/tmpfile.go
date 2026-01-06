package utils

import (
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/pachirode/pkg/log"
)

var (
	tmpFiles     = make(map[string]*tmpMeta)
	mu           sync.Mutex
	cleanupAfter = 10 * time.Minute

	once     sync.Once
	stopOnce sync.Once
	stopCh   = make(chan struct{})
	wg       sync.WaitGroup
)

type tmpMeta struct {
	Path    string
	Created time.Time
	State   TmpState
	Ref     int // 读取引用计数
}

func RegisterTmp(id string, path string) {
	meta := &tmpMeta{
		Path:    path,
		Created: time.Now(),
		State:   StateReady,
		Ref:     0,
	}
	mu.Lock()
	defer mu.Unlock()
	tmpFiles[id] = meta
}

func MarkInReading(id string) error {
	mu.Lock()
	defer mu.Unlock()

	if tmpFiles[id].State == StateReady || tmpFiles[id].State == StateReading {
		tmpFiles[id].State = StateReading
		tmpFiles[id].Ref++
		return nil
	}

	return fmt.Errorf("Current State %v, can not convert %v", tmpFiles[id].State, StateReading)
}

func MarkInRunning(id string) error {
	mu.Lock()
	defer mu.Unlock()

	if tmpFiles[id].State == StateReady {
		tmpFiles[id].State = StateRunning
		return nil
	}

	return fmt.Errorf("Current State %v, can not convert %v", tmpFiles[id].State, StateRunning)
}

func MarkReleased(id string) error {
	mu.Lock()
	defer mu.Unlock()

	if tmpFiles[id].State == StateReady || tmpFiles[id].State == StateRunning {
		tmpFiles[id].State = StateReady
		return nil
	}

	if tmpFiles[id].State == StateReading {
		if tmpFiles[id].Ref > 1 {
			tmpFiles[id].Ref--
			return nil
		} else {
			tmpFiles[id].Ref = 0
			tmpFiles[id].State = StateReady
			return nil
		}
	}

	return nil
}

func UnregisterTmp(file string) {
	mu.Lock()
	defer mu.Unlock()
	delete(tmpFiles, file)
}

func StartCleanup(interval time.Duration) {
	once.Do(func() {
		wg.Add(1)
		go func() {
			defer wg.Done()

			ticker := time.NewTicker(interval)
			defer ticker.Stop()

			for {
				select {
				case <-ticker.C:
					cleanup(false)
				case <-stopCh:
					return
				}
			}
		}()
	})
}

func ShutdownCleanup() {
	cleanup(true)

	stopOnce.Do(func() {
		close(stopCh)
	})

	wg.Wait()
}

func cleanup(force bool) {
	now := time.Now()

	mu.Lock()
	defer mu.Unlock()

	for path, meta := range tmpFiles {

		if meta.State != StateReady {
			continue
		}

		if force || now.Sub(meta.Created) >= cleanupAfter {
			_ = os.Remove(path)
			delete(tmpFiles, path)
		}
	}
}

func DumpTmpFiles() {
	mu.Lock()
	defer mu.Unlock()

	for path, meta := range tmpFiles {
		log.Infow(
			"tmpfile",
			"path", path,
			"created", meta.Created.Format(time.RFC3339Nano),
			"age", time.Since(meta.Created).String(),
			"state", meta.State,
		)
	}
}
