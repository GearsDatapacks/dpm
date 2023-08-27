package main

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"os"

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

	if exists("README.md") {
		bytes, err := os.ReadFile("README.md")

		if err != nil {
			log.Fatal(err)
		}

		body = string(bytes)
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
		
		err := modrinthProject.Modify(gorinth.Project{
			Title: project.Name,
			Description: project.Summary,
			Body: body,
			Categories: project.Categories,
			License: gorinth.License{
				Id: project.License,
			},
		}, auth)

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

	err = user.CreateProject(gorinth.Project{
		Slug: slug,
		Title: project.Name,
		Description: project.Summary,
		Categories: project.Categories,
		ClientSide: "optional",
		ServerSide: "required",
		Body: body,
		ProjectType: "mod",
		Status: "draft",
		GameVersions: project.GameVersions,
		Loaders: []string{"datapack"},
	})

	if err != nil {
		log.Fatal(err)
	}

	fmt.Printf("Successfully created project %q\n", project.Name)
}

var includedFiles = []string{
	"pack.png",
	"README.md",
	"CHANGELOG.md",
	"LICENSE.md",
}

func publishVersion(metadata projectJson, auth string) {
	title := metadata.Name
	versionNumber := metadata.Version
	dependencies := formatDependencies(metadata.Dependencies, auth)

	versionTitle := fmt.Sprintf("%s-v%s", title, versionNumber)
	
	fmt.Println(versionNumber, versionTitle)

	zipPath := versionTitle + ".zip"

	filesToZip := []string{"data", "pack.mcmeta"}

	for _, file := range includedFiles {
		if exists(file) {
			filesToZip = append(filesToZip, file)
		}
	}

	zipFiles(zipPath, filesToZip)

	project, err := gorinth.GetProject(metadata.Slug, auth)

	if err != nil {
		log.Fatal(err)
	}

	version := gorinth.Version{
		Name: versionTitle,
		VersionNumber: versionNumber,
		Dependencies: dependencies,
		GameVersions: metadata.GameVersions,
		VersionType: metadata.ReleaseType,
		Loaders: []string{ "datapack" },
		FileParts: []string{ zipPath },
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
			ProjectId: dependency.Id,
			VersionId: version.Id,
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
