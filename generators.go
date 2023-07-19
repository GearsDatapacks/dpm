package main

import (
	"fmt"
	"strings"
)

func initProject() {
	if exists("project.json") {
		fmt.Println("File project.json already exists.")
		return
	}

	title := prompt("Title of project: ")
	slug := prompt(fmt.Sprintf("Project slug (%s): ", toSlug(title)))
	version := prompt("Current version (0.1.0): ")
	gameVersions := strings.Split(prompt("Enter space separated compatible game versions: "), " ")
	summary := prompt("Summary of datapack: ")
	license := prompt("Project license (GPL-3.0): ")

	if slug == "" {
		slug = toSlug(title)
	}
	if version == "" {
		version = "0.1.0"
	}
	if license == "" {
		license = "GPL-3.0"
	}

	project := projectJson{
		Name: title,
		Slug: slug,
		Version: version,
		GameVersions: gameVersions,
		Summary: summary,
		License: license,
		Categories: []string{},
		Dependencies: map[string]string{},
		ReleaseType: "release",
	}

	setProjectJson(project)
}
