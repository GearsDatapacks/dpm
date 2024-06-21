package modrinth

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"slices"
	"strings"
	"time"

	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
	"github.com/gearsdatapacks/gorinth"
)

var downloaded = []string{}

func Install(context types.Context, depKind string) {
	downloaded = []string{}
	if len(context.Values) == 0 {
		downloadDependencies(context.Auth, depKind)
	}

	for _, projectStr := range context.Values {
		project, version := getVersion(projectStr, context.Auth)
		fmt.Printf("Project %q found\n", project.Title)

		if utils.Exists("project.json") {
			addDependency(version, project.Slug, depKind)
		}

		downloadVersion(version)
	}
}

func addDependency(dependency gorinth.Version, slug string, depKind string) {
	project := utils.GetProjectJson()
	if depKind == "dev" {
		if project.DevDependencies == nil {
			project.DevDependencies = map[string]string{}
		}

		project.DevDependencies[slug] = dependency.VersionNumber
	} else if depKind == "optional" {
		if project.OptionalDependencies == nil {
			project.OptionalDependencies = map[string]string{}
		}

		project.OptionalDependencies[slug] = dependency.VersionNumber
	} else {
		if project.Dependencies == nil {
			project.Dependencies = map[string]string{}
		}

		project.Dependencies[slug] = dependency.VersionNumber
	}

	utils.SetProjectJson(project)
}

func getVersion(projectStr, auth string) (gorinth.Project, gorinth.Version) {
	values := strings.Split(projectStr, "@")
	projectId := values[0]
	versionId := ""
	if len(values) > 1 {
		versionId = values[1]
	}
	project, err := gorinth.GetProject(projectId, auth)

	if err != nil {
		log.Fatal(err)
	}

	if versionId == "" {
		return project, getLatestStable(project)
	} else if versionId == "latest" {
		return project, project.GetLatestVersion()
	} else {
		return project, project.GetSpecificVersion(versionId)
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

func downloadDependencies(auth string, depKind string) {
	project := utils.GetProjectJson()
	deps := project.Dependencies
	if depKind == "dev" {
		deps = project.DevDependencies
	} else if depKind == "optional" {
		deps = project.OptionalDependencies
	}

	if deps == nil {
		return
	}

	for slug, versionNumber := range deps {
		dependencyProject, err := gorinth.GetProject(slug, auth)

		if err != nil {
			log.Fatal(err)
		}

		requiredVersion := dependencyProject.GetSpecificVersion(versionNumber)

		downloadVersion(requiredVersion)
	}
}

func downloadVersion(version gorinth.Version) {
	if slices.Contains(downloaded, version.Id) {
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
	if utils.Exists("project.json") {
		filename = "../" + filename
	}

	if utils.Exists(filename) {
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
