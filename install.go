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
	if len(projects) == 0 {
		downloadDependencies(auth)
	}

	for _, project := range projects {
		if exists("project.json") {
			addDependency(project, auth)
		}

		downloadProject(project, auth)
	}
}

func addDependency(dependency string, auth string) {
	project := getProjectJson()

	dependencyProject, err := gorinth.GetProject(dependency, auth)

	if err != nil {
		log.Fatal(err)
	}

	latestVersion := dependencyProject.GetLatestVersion().VersionNumber

	if project.Dependencies == nil {
		project.Dependencies = map[string]string{}
	}

	project.Dependencies[dependency] = latestVersion

	setProjectJson(project)
}

func downloadProject(project_id string, auth string) {
	project, err := gorinth.GetProject(project_id, auth)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Project %q found\n", project.Title)

	latest := project.GetLatestVersion()

	downloadVersion(latest)
}

func downloadDependencies(auth string) {
	project := getProjectJson()

	for slug, versionNumber := range project.Dependencies {
		dependencyProject, err := gorinth.GetProject(slug, auth)

		if err != nil {
			log.Fatal(err)
		}

		requiredVersion := dependencyProject.GetSpecificVersion(versionNumber)

		downloadVersion(requiredVersion)
	}
}

func downloadVersion(version gorinth.Version) {
	files := version.Files

	for _, file := range files {
		skipped := downloadFile(file)

		if skipped {
			return
		}
	}

	for _, dependency := range version.Dependencies {
		downloadVersion(dependency.GetVersion())
	}
}

func downloadFile(downloadFile gorinth.File) (skipped bool) {
	filename := downloadFile.Filename

	if exists(filename) {
		fmt.Printf("File %s already exists, skipping...\n", filename)
		return true
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

	fmt.Printf("%s downloaded in %v.\n", formatSize(size), totalTime.Round(time.Second/10))

	return false
}

func formatSize(bytes int64) string {
	const MEGABYTE = 1024 * 1024
	const KILOBYTE = 1024

	if bytes > MEGABYTE {
		return fmt.Sprintf("%vMB", bytes/MEGABYTE)
	} else if bytes > KILOBYTE {
		return fmt.Sprintf("%vKB", bytes/KILOBYTE)
	} else {
		return fmt.Sprintf("%vB", bytes)
	}
}
