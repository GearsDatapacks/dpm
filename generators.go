package main

import (
	"encoding/json"
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

	config := dpmConfig{
		IncludeFiles: []string{},
		ExcludeFiles: []string{},
	}

	bytes, _ := json.MarshalIndent(config, "", "  ")
	err := os.WriteFile("dpmconfig.json", bytes, 0666)
	if err != nil {
		log.Fatal(err)
	}

	if project.Name == "" {
		project.Name = prompt("Title of project: ")
	} else {
		name := prompt("Title of project (" + project.Name + "): ")
		if name != "" {
			project.Name = name
		}
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
	if project.ReleaseType == "" {
		project.ReleaseType = "release"
	}
	if project.Categories == nil {
		project.Categories = []string{}
	}
	if project.AditionalCategories == nil {
		project.AditionalCategories = []string{}
	}
	if project.Dependencies == nil {
		project.Dependencies = map[string]string{}
	}
	if project.Version == "" {
		project.Version = DPM_VERSION.String()
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
	case "simple":
		createSimple(name)
	default:
		log.Fatalf("Unrecognised template name %q", template)
	}
}

func writeFile(path string, content string) {
	err := os.WriteFile(path, []byte(content), 0666)
	if err != nil {
		log.Fatal(err)
	}
}

func createBasic(name string) projectJson {
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

	writeFile(joinPath("data", "minecraft", "tags", "functions", "tick.json"), makeTagFile(namespace+":tick"))
	writeFile(joinPath("data", "minecraft", "tags", "functions", "load.json"), makeTagFile(namespace+":load"))

	err = os.MkdirAll(joinPath("data", namespace, "functions"), 0777)
	if err != nil {
		log.Fatal(err)
	}

	writeFile(joinPath("data", namespace, "functions", "load.mcfunction"), fmt.Sprintf(`tellraw @a "Loaded %s v%s"`, project.Name, project.Version))
	writeFile(joinPath("data", namespace, "functions", "tick.mcfunction"), "")

	return project
}

const LOAD_TEXT = `function %s:objectives
function %s:version
`

const VERSION_TEXT = `data modify storage %s:version version set value "%s"
tellraw @a ["%s v", {"storage":"%s:version","nbt":"version"}]
`

func createSimple(name string) {
	project := createBasic(name)

	namespace := toNamespace(name)

	writeFile(joinPath("data", namespace, "functions", "load.mcfunction"), fmt.Sprintf(LOAD_TEXT, namespace, namespace))
	writeFile(joinPath("data", namespace, "functions", "version.mcfunction"), fmt.Sprintf(VERSION_TEXT, namespace, project.Version, project.Name, namespace))
	writeFile(joinPath("data", namespace, "functions", "objectives.mcfunction"), "")
}
