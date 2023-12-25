package main

import (
	"archive/zip"
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"

	"github.com/gearsdatapacks/gorinth"
)

func publish(auth string) {
	if auth == "" {
		log.Fatal("Please specify --auth to publish a project")
	}

	project := getProjectJson()
	projectVersion := ParseVersion(project.DpmVersion)
	reader := bufio.NewReader(os.Stdin)
	if projectVersion.Less(DPM_VERSION) {
		fmt.Print("[Warning] This project was made with an older version of DPM and may use a different project format.\nPress CTRL+C to quit or enter to continue anyway.")
		reader.ReadLine()
	}
	if projectVersion.Greater(DPM_VERSION) {
		fmt.Println("[Warning] This project was made with an newer version of DPM and may use a different project format. Consider updating DPM.\nPress CTRL+C to quit or enter to continue anyway.")
		reader.ReadLine()
	}

	slug := project.Slug
	if slug == "" {
		slug = toSlug(project.Name)
	}

	modrinthProject, err := gorinth.GetProject(slug, auth)

	body := modrinthProject.Body

	if filename := findFile(".", "README*", []string{}); filename != "" {
		bytes, err := os.ReadFile(filename)

		if err != nil {
			log.Fatal(err)
		}

		body = string(bytes)
	}

	var icon []byte

	if exists("pack.png") {
		icon, err = os.ReadFile("pack.png")
		if err != nil {
			log.Fatal(err)
		}
	}

	// If the project exists, modify it
	if err == nil {
		versions := modrinthProject.GetVersions()

		hasVersion := false

		for _, version := range versions {
			if version.VersionNumber == project.Version {
				hasVersion = true
				break
			}
		}

		modified := gorinth.Project{
			Title:                project.Name,
			Description:          project.Summary,
			Body:                 body,
			Categories:           project.Categories,
			AdditionalCategories: project.AdditionalCategories,
			License: &gorinth.License{
				Id: project.License,
			},
		}

		if icon != nil {
			modified.Icon = icon
		}

		err := modrinthProject.Modify(modified, auth)

		if err != nil {
			log.Fatal(err)
		}

		fmt.Printf("Successfully updated project %s\n", modrinthProject.Title)
		if !hasVersion {
			publishVersion(project, auth)
		}
		return
	}
	// Otherwise, make a new one
	user := gorinth.GetUserFromAuth(auth)

	toPublish := gorinth.Project{
		Slug:         slug,
		Title:        project.Name,
		Description:  project.Summary,
		Categories:   project.Categories,
		ClientSide:   "optional",
		ServerSide:   "required",
		Body:         body,
		ProjectType:  "mod",
		Status:       "draft",
		GameVersions: project.GameVersions,
		Loaders:      []string{"datapack"},
		License: &gorinth.License{
			Id: project.License,
		},
	}

	if icon != nil {
		toPublish.Icon = icon
	}

	err = user.CreateProject(toPublish)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Successfully created project %q\n", project.Name)

	publishVersion(project, auth)
}

func findFile(dir, pattern string, excludeFiles []string) string {
	files, err := os.ReadDir(dir)
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range files {
		if file.IsDir() {
			continue
		}
		matched, err := filepath.Match(pattern, file.Name())
		if err != nil {
			log.Fatal(err)
		}

		if !matched {
			continue
		}

		matchedExclude := false
		for _, exclude := range excludeFiles {
			matched, err := filepath.Match(exclude, file.Name())
			if err != nil {
				log.Fatal(err)
			}
			if matched {
				matchedExclude = true
			}
		}

		if !matchedExclude {
			return file.Name()
		}
	}

	return ""
}

func publishVersion(metadata projectJson, auth string) {
	title := metadata.Name
	versionNumber := metadata.Version
	dependencies := formatDependencies(metadata.Dependencies, auth)

	versionTitle := fmt.Sprintf("%s-v%s", title, versionNumber)

	zipPath := versionTitle + ".zip"

	filesToZip := []string{"data", "pack.mcmeta"}

	includedFiles := []string{
		"pack.png",
		"README*",
		"CHANGELOG*",
		"LICENSE*",
	}
	excludedFiles := []string{}

	config, hasConfig := getConfig()

	if hasConfig {
		includedFiles = append(includedFiles, config.IncludeFiles...)
		excludedFiles = config.ExcludeFiles
	}

	for _, file := range includedFiles {
		if filename := findFile(".", file, excludedFiles); filename != "" {
			filesToZip = append(filesToZip, filename)
		}
	}

	zipFiles(zipPath, filesToZip)

	project, err := gorinth.GetProject(metadata.Slug, auth)

	if err != nil {
		log.Fatal(err)
	}

	version := gorinth.Version{
		Name:          versionTitle,
		VersionNumber: versionNumber,
		Dependencies:  dependencies,
		GameVersions:  metadata.GameVersions,
		VersionType:   metadata.ReleaseType,
		Loaders:       []string{"datapack"},
		FileParts:     []string{zipPath},
	}

	err = project.CreateVersion(version, auth)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Successfully created version %q\n", versionTitle)
}

func formatDependencies(dependencies map[string]string, auth string) []gorinth.Dependency {
	result := []gorinth.Dependency{}

	for slug, versionNumber := range dependencies {
		dependency, err := gorinth.GetProject(slug, auth)
		if err != nil {
			log.Fatal(err)
		}
		version := dependency.GetSpecificVersion(versionNumber)

		formatted := gorinth.Dependency{
			ProjectId:      dependency.Id,
			VersionId:      version.Id,
			DependencyType: "required",
		}

		result = append(result, formatted)
	}

	return result
}

func zipFiles(filename string, files []string) {
	archive, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer archive.Close()

	zipWriter := zip.NewWriter(archive)
	defer zipWriter.Close()

	for _, fileToZip := range files {
		if isDir(fileToZip) {
			zipDir(zipWriter, fileToZip)
		} else {
			zipFile(zipWriter, fileToZip)
		}
	}
}

func zipFile(writer *zip.Writer, fileToZip string) {
	file, err := os.Open(fileToZip)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	zipped, err := writer.Create(fileToZip)
	if err != nil {
		log.Fatal(err)
	}

	_, err = io.Copy(zipped, file)
	if err != nil {
		log.Fatal(err)
	}
}

func zipDir(writer *zip.Writer, dir string) {
	files, err := os.ReadDir(dir)
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range files {
		path := fmt.Sprintf("%s/%s", dir, file.Name())
		if file.IsDir() {
			zipDir(writer, path)
		} else {
			zipFile(writer, path)
		}
	}
}
