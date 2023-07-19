package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gearsdatapacks/gorinth"
)

func install(projects []string, auth string) {
	for _, project := range projects {
		downloadProject(project, auth)
	}
}

func downloadProject(project_id string, auth string) {
	project := gorinth.GetProject(project_id, auth)

	fmt.Printf("Project %q found\n", project.Title)

	latest := project.GetLatestVersion()

	versionsToDownload := []gorinth.Version{latest}

	for _, dependency := range latest.Dependencies {
		versionsToDownload = append(versionsToDownload, dependency.GetVersion())
	}

	for _, version := range versionsToDownload {
		downloadVersion(version)
	}
}

func downloadVersion(version gorinth.Version) {
	files := version.Files

	for _, file := range files {
		downloadFile(file)
	}
}

func downloadFile(downloadFile gorinth.File) {
	filename := downloadFile.Filename

	if exists(filename) {
		fmt.Printf("File %s already exists, skipping...\n", filename)
		return
	}

	fmt.Printf("Downloading file %s... ", filename)
	startTime := time.Now()
	file, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)
	}

	client := http.Client{
		CheckRedirect: func(r *http.Request, via []*http.Request) error {
				r.URL.Opaque = r.URL.Path
				return nil
		},
	}
	response, err := client.Get(downloadFile.Url)
	if err != nil {
			log.Fatal(err)
	}
	defer response.Body.Close()

	size, err := io.Copy(file, response.Body)

	if err != nil {
		log.Fatal(err)
	}

	endTime := time.Now()
	totalTime := endTime.Sub(startTime)

	defer file.Close()

	fmt.Printf("%s downloaded in %v.\n", formatSize(size), totalTime.Round(time.Second / 10))
}

func formatSize(bytes int64) string {
	const MEGABYTE = 1024 * 1024
	const KILOBYTE = 1024

	if bytes > MEGABYTE {
		return fmt.Sprintf("%vMB", bytes / MEGABYTE)
	} else if bytes > KILOBYTE {
		return fmt.Sprintf("%vKB", bytes / KILOBYTE)
	} else {
		return fmt.Sprintf("%vB", bytes)
	}
}
