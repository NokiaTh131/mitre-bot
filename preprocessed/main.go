package main

import (
	"encoding/json"
	"log"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"sync"
)

const (
	dir        = "./attack-pattern/"
	outputFile = "attack-patterns.json"
)

func worker(jobs <-chan string, results chan<- Bundle) {
	for path := range jobs {
		file, err := os.Open(path)
		if err != nil {
			log.Println(err)
			continue
		}

		var b Bundle
		if err := json.NewDecoder(file).Decode(&b); err != nil {
			file.Close()
			log.Println(err)
			continue
		}
		file.Close()
		results <- b
	}
}

func writeFile(bundles []AttackPattern) error {
	jsonBytes, err := json.MarshalIndent(bundles, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(outputFile, jsonBytes, 0o644)
}

func main() {
	numWorkers := runtime.NumCPU()
	jobs := make(chan string, 1000)
	results := make(chan Bundle, 1000)
	var wg sync.WaitGroup
	for range numWorkers {
		wg.Go(func() {
			worker(jobs, results)
		})
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	go func() {
		filepath.WalkDir(dir, func(path string, d os.DirEntry, err error) error {
			if err == nil && !d.IsDir() && strings.HasSuffix(strings.ToLower(d.Name()), ".json") {
				jobs <- path
			}
			return nil
		})
		close(jobs)
	}()

	var attackPatterns []AttackPattern
	for b := range results {
		for _, obj := range b.Objects {
			if obj.Type != "attack-pattern" {
				continue
			}

			atkPat := AttackPattern{
				ID:          obj.ID,
				Name:        obj.Name,
				Description: obj.Description,
				Platforms:   obj.XMitrePlatforms,
			}

			attackPatterns = append(attackPatterns, atkPat)
		}
	}
	if err := writeFile(attackPatterns); err != nil {
		panic(err)
	}
}
