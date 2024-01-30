package main

import (
	"fmt"
	"os"

	"github.com/gearsdatapacks/gorinth"
)

func uninstall(projects []string, auth string, depKind string) {
	if !exists("project.json") {
		fmt.Println("Must be in an intitialised project to uninstall dependencies")
		return
	}
	projectJson := getProjectJson()
	deps := projectJson.Dependencies
	if depKind == "dev" {
		deps = projectJson.DevDependencies
	} else	if depKind == "optional" {
		deps = projectJson.OptionalDependencies
	}

	if deps == nil {
		return
	}

	for _, slug := range projects {
		versionNumber, hasDep := deps[slug]
		if !hasDep {
			fmt.Printf("Project %s is not installed\n", slug)
			continue
		}
		delete(deps, slug)
		project, version := getVersion(slug + "@" + versionNumber, auth)
		fmt.Printf("Uninstalling project %s\n", project.Title)
		uninstallVersion(version)
	}

	if depKind == "dev" {
		projectJson.DevDependencies = deps
	} else	if depKind == "optional" {
		projectJson.OptionalDependencies = deps
	} else {
		projectJson.Dependencies = deps
	}

	setProjectJson(projectJson)
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
