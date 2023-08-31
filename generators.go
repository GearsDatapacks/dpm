package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

func initProject() {
	createProject(projectJson{})
}

func createProject(project projectJson) projectJson {
	if exists("project.json") {
		log.Fatal("File project.json already exists.")
		return project
	}

	if project.Name == "" {
		project.Name = prompt("Title of project: ")
	}
	if project.Slug == "" {
		project.Slug = prompt(fmt.Sprintf("Project slug (%s): ", toSlug(project.Name)))
	}
	if project.Version == "" {
		project.Version = prompt("Current version (0.1.0): ")
	}
	if project.GameVersions == nil {
		project.GameVersions = strings.Split(prompt("Enter space separated compatible game versions: "), " ")
	}
	if project.Summary == "" {
		project.Summary = prompt("Summary of datapack: ")
	}
	if project.License == "" {
		project.License = prompt("Project license (GPL-3.0): ")
	}

	if project.Slug == "" {
		project.Slug = toSlug(project.Name)
	}
	if project.Version == "" {
		project.Version = "0.1.0"
	}
	if project.License == "" {
		project.License = "GPL-3.0"
	}

	setProjectJson(project)
	return project
}

const PACK_FORMAT = "17"
func makeMcmeta(desc string) string {
	return `{
	"pack": {
		"pack_format": ` + PACK_FORMAT + `,
		"description": "` + desc + `"
	}
}`
}

func makeTagFile(name string) string {
return fmt.Sprintf(`{
	"values": [
		"%s"
	]
}`, name)
}

func createTemplate(template string, name string) {
	switch strings.ToLower(template) {
	case "basic":
		createBasic(name)
	default:
		log.Fatalf("Unrecognised template name %q", template)
	}
}

func createBasic(name string) {
	err := os.Mkdir(name, 0777)
	if err != nil {
		log.Fatal(err)
	}
	err = os.Chdir(name)
	if err != nil {
		log.Fatal(err)
	}

	project := createProject(projectJson{Name: name})
	namespace := toNamespace(name)
	mcmeta := makeMcmeta(fmt.Sprintf("%s v%s", project.Name, project.Version))

	os.WriteFile("pack.mcmeta", []byte(mcmeta), 0666)
	
	err = os.MkdirAll(joinPath("data", "minecraft", "tags", "functions"), 0777)
	if err != nil {
		log.Fatal(err)
	}
	
	err = os.WriteFile(joinPath("data", "minecraft", "tags", "functions", "tick.json"), []byte(makeTagFile(namespace + ":tick")), 0666)
	if err != nil {
		log.Fatal(err)
	}
	err = os.WriteFile(joinPath("data", "minecraft", "tags", "functions", "load.json"), []byte(makeTagFile(namespace + ":load")), 0666)
	if err != nil {
		log.Fatal(err)
	}

	err = os.MkdirAll(joinPath("data", namespace, "functions"), 0777)
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(joinPath("data", namespace, "functions", "tick.mcfunction"), []byte(fmt.Sprintf(`tellraw @a "Loaded %s v%s"`, project.Name, project.Version)), 0666)
	if err != nil {
		log.Fatal(err)
	}
	_, err = os.Create(joinPath("data", namespace, "functions", "load.mcfunction"))
	if err != nil {
		log.Fatal(err)
	}
}
