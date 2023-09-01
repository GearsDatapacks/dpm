package main

import (
	"archive/zip"
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

	slug := project.Slug
	if slug == "" {
		slug = toSlug(project.Name)
	}

	modrinthProject, err := gorinth.GetProject(slug, auth)

	body := modrinthProject.Body

	if filename := findFile(".", "README*"); filename != "" {
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
			Title:       project.Name,
			Description: project.Summary,
			Body:        body,
			Categories:  project.Categories,
			License: gorinth.License{
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
	}

	if icon != nil {
		toPublish.Icon = icon
	}

	err = user.CreateProject(toPublish)

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Successfully created project %q\n", project.Name)
}

func findFile(dir, pattern string) string {
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
		if matched {
			return file.Name()
		}
	}

	return ""
}

var includedFiles = []string{
	"pack.png",
	"README*",
	"CHANGELOG*",
	"LICENSE*",
}

func publishVersion(metadata projectJson, auth string) {
	title := metadata.Name
	versionNumber := metadata.Version
	dependencies := formatDependencies(metadata.Dependencies, auth)

	versionTitle := fmt.Sprintf("%s-v%s", title, versionNumber)

	zipPath := versionTitle + ".zip"

	filesToZip := []string{"data", "pack.mcmeta"}

	for _, file := range includedFiles {
		if filename := findFile(".", file); filename != "" {
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
