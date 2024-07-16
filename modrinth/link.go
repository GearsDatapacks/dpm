package modrinth

import (
	"log"

	"github.com/gearsdatapacks/dpm/project"
	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
	"github.com/gearsdatapacks/gorinth"
)

func Link(context types.Context) {
	modrinthProject, err := gorinth.GetProject(context.Values[0], context.Auth)
	if err != nil {
		log.Fatal(err)
	}

	version := modrinthProject.GetLatestVersion()

	var projectData types.Project
	if utils.Exists("project.json") {
		log.Fatal("project.json already exists")
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
