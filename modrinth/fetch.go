package modrinth

import (
	"archive/zip"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"strings"

	"github.com/gearsdatapacks/dpm/project"
	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
	"github.com/gearsdatapacks/gorinth"
)

func Fetch(context types.Context) {
	modrinthProject, version := getVersion(context.Values[0], context.Auth)

	err := os.MkdirAll(modrinthProject.Title, os.ModePerm)
	if err != nil {
		log.Fatal(err)
	}
	err = os.Chdir(modrinthProject.Title)
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range version.Files {
		downloadFile(file)
	}

	mainFile := version.Files[0].Filename
	err = unzip(mainFile)
	if err != nil {
		log.Fatal(err)
	}

	// Only generate project.json if it the datapack doesn't include it
	var projectData types.Project
	if utils.Exists("project.json") {
		projectData = utils.GetProjectJson()
	} else {
		projectData = types.Project{
			Name:                 modrinthProject.Title,
			Slug:                 modrinthProject.Slug,
			Version:              version.VersionNumber,
			GameVersions:         version.GameVersions,
			Summary:              modrinthProject.Description,
			License:              modrinthProject.License.Id,
			Categories:           modrinthProject.Categories,
			AdditionalCategories: modrinthProject.AdditionalCategories,
			Dependencies:         map[string]string{},
			DevDependencies:      map[string]string{},
			OptionalDependencies: map[string]string{},
			ReleaseType:          version.VersionType,
		}

		for _, dep := range version.Dependencies {
			depVersion := dep.GetVersion()
			depProject, err := gorinth.GetProject(dep.ProjectId, context.Auth)
			if err != nil {
				log.Fatal(err)
			}

			if dep.DependencyType == "required" {
				projectData.Dependencies[depProject.Slug] = depVersion.VersionNumber
			} else if dep.DependencyType == "optional" {
				projectData.OptionalDependencies[depProject.Slug] = depVersion.VersionNumber
			}
		}

		project.CreateProject(projectData, true)
	}
}

func unzip(filename string) error {
	reader, err := zip.OpenReader(filename)
	if err != nil {
		return err
	}
	defer reader.Close()

	destination, err := filepath.Abs(".")
	if err != nil {
		return err
	}

	for _, f := range reader.File {
		err := unzipFile(f, destination)
		if err != nil {
			return err
		}
	}

	return nil
}

func unzipFile(f *zip.File, destination string) error {
	filePath := filepath.Join(destination, f.Name)
	if !strings.HasPrefix(filePath, filepath.Clean(destination)+string(os.PathSeparator)) {
		return fmt.Errorf("invalid file path: %s", filePath)
	}

	if f.FileInfo().IsDir() {
		if err := os.MkdirAll(filePath, os.ModePerm); err != nil {
			return err
		}
		return nil
	}

	if err := os.MkdirAll(filepath.Dir(filePath), os.ModePerm); err != nil {
		return err
	}

	destinationFile, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_TRUNC, f.Mode())
	if err != nil {
		return err
	}
	defer destinationFile.Close()

	zippedFile, err := f.Open()
	if err != nil {
		return err
	}
	defer zippedFile.Close()

	if _, err := io.Copy(destinationFile, zippedFile); err != nil {
		return err
	}
	return nil
}
