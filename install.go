package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gearsdatapacks/gorinth"
)

var downloaded = []string{}

func install(projects []string, auth string) {
	downloaded = []string{}
	if len(projects) == 0 {
		downloadDependencies(auth)
	}

	for _, projectStr := range projects {
		values := strings.Split(projectStr, "@")
		id := values[0]
		version_id := ""
		if len(values) > 1 {
			version_id = values[1]
		}

		project, version := getVersion(id, version_id, auth)
		fmt.Printf("Project %q found\n", project.Title)

		if exists("project.json") {
			addDependency(version, id, auth)
		}

		downloadVersion(version)
	}
}

func addDependency(dependency gorinth.Version, slug string, auth string) {
	project := getProjectJson()

	if project.Dependencies == nil {
		project.Dependencies = map[string]string{}
	}

	project.Dependencies[slug] = dependency.VersionNumber

	setProjectJson(project)
}

func downloadProject(project_id, version_id, auth string) {
	project, err := gorinth.GetProject(project_id, auth)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Project %q found\n", project.Title)

	var version gorinth.Version

	if version_id == "" {
		version = getLatestStable(project)
	} else if version_id == "latest" {
		version = project.GetLatestVersion()
	} else {
		version = project.GetSpecificVersion(version_id)
	}

	downloadVersion(version)
}

func getVersion(project_id, version_id, auth string) (gorinth.Project, gorinth.Version) {
	project, err := gorinth.GetProject(project_id, auth)

	if err != nil {
		log.Fatal(err)
	}

	if version_id == "" {
		return project, getLatestStable(project)
	} else if version_id == "latest" {
		return project, project.GetLatestVersion()
	} else {
		return project, project.GetSpecificVersion(version_id)
	}
}

func getLatestStable(project gorinth.Project) gorinth.Version {
	for _, version := range project.GetVersions() {
		if version.VersionType == "release" {
			return version
		}
	}

	log.Printf("Warning: Project %q has no stable versions, defaulting to latest\n", project.Title)
	return project.GetLatestVersion()
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
	if contains(downloaded, version.Id) {
		return
	}
	downloaded = append(downloaded, version.Id)

	files := version.Files

	for _, file := range files {
		downloadFile(file)
	}

	for _, dependency := range version.Dependencies {
		if dependency.DependencyType != "required" {
			continue
		}

		downloadVersion(dependency.GetVersion())
	}
}

func downloadFile(downloadFile gorinth.File) {
	filename := downloadFile.Filename
	if exists("project.json") {
		filename = "../" + filename
	}

	if exists(filename) {
		fmt.Printf("File %s already exists, skipping...\n", downloadFile.Filename)
		return
	}

	fmt.Printf("Downloading file %s... ", downloadFile.Filename)
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
