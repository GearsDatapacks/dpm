package modrinth

import (
	"fmt"
	"os"

	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
	"github.com/gearsdatapacks/gorinth"
)

func Uninstall(context types.Context, depKind string) {
	if !utils.Exists("project.json") {
		fmt.Println("Must be in an intitialised project to uninstall dependencies")
		return
	}
	projectJson := utils.GetProjectJson()
	deps := projectJson.Dependencies
	if depKind == "dev" {
		deps = projectJson.DevDependencies
	} else if depKind == "optional" {
		deps = projectJson.OptionalDependencies
	}

	if deps == nil {
		return
	}

	for _, slug := range context.Values {
		versionNumber, hasDep := deps[slug]
		if !hasDep {
			fmt.Printf("Project %s is not installed\n", slug)
			continue
		}
		delete(deps, slug)
		project, version := getVersion(slug+"@"+versionNumber, context.Auth)
		fmt.Printf("Uninstalling project %s\n", project.Title)
		uninstallVersion(version)
	}

	if depKind == "dev" {
		projectJson.DevDependencies = deps
	} else if depKind == "optional" {
		projectJson.OptionalDependencies = deps
	} else {
		projectJson.Dependencies = deps
	}

	utils.SetProjectJson(projectJson)
}

func uninstallVersion(version gorinth.Version) {
	for _, file := range version.Files {
		os.Remove("../" + file.Filename)
	}

	for _, dependency := range version.Dependencies {
		if dependency.DependencyType == "required" {
			uninstallVersion(dependency.GetVersion())
		}
	}
}
