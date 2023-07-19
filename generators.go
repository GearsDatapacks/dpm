package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"
)

func init() {
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

	byteStream, err := json.MarshalIndent(project, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("project.json", byteStream, 0666)

	if err != nil {
		log.Fatal(err)
	}
}
