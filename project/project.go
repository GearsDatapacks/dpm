package project

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path"
	"slices"
	"strings"

	"github.com/gearsdatapacks/dpm/settings"
	"github.com/gearsdatapacks/dpm/types"
	"github.com/gearsdatapacks/dpm/utils"
)

func InitProject() {
	CreateProject(types.Project{})
}

func CreateProject(project types.Project, noPrompt ...bool) types.Project {
	shouldPrompt := true
	if len(noPrompt) > 0 {
		shouldPrompt = !noPrompt[0]
	}

	if utils.Exists("project.json") {
		fmt.Println("File project.json already exists.")
		return project
	}

	if !utils.Exists("dpmconfig.json") {
		config := types.Config{
			IncludeFiles: []string{},
			ExcludeFiles: []string{},
		}

		bytes, _ := json.MarshalIndent(config, "", "  ")
		err := os.WriteFile("dpmconfig.json", bytes, 0666)
		if err != nil {
			log.Fatal(err)
		}
	}

	if project.Name != "" && shouldPrompt {
		name := utils.Prompt("Title of project (" + project.Name + "): ")
		if name != "" {
			project.Name = name
		}
	}
	project = setProjectValues(project)

	utils.SetProjectJson(project)
	return project
}

func setProjectValues(project types.Project) types.Project {
	if project.Name == "" {
		project.Name = utils.Prompt("Title of project: ")
	}
	if project.Slug == "" {
		project.Slug = utils.Prompt(fmt.Sprintf("Project slug (%s): ", utils.ToSlug(project.Name)))
	}
	if project.Version == "" {
		project.Version = utils.Prompt("Current version (0.1.0): ")
	}
	if project.GameVersions == nil {
		project.GameVersions = strings.Split(utils.Prompt("Enter space separated compatible game versions: "), " ")
	}
	if project.Summary == "" {
		project.Summary = utils.Prompt("Summary of datapack: ")
	}
	if project.License == "" {
		project.License = utils.Prompt("Project license (GPL-3.0): ")
	}
	if project.ReleaseType == "" {
		project.ReleaseType = "release"
	}
	if project.Categories == nil {
		project.Categories = []string{}
	}
	if project.AdditionalCategories == nil {
		project.AdditionalCategories = []string{}
	}
	if project.Dependencies == nil {
		project.Dependencies = map[string]string{}
	}
	if project.DevDependencies == nil {
		project.DevDependencies = map[string]string{}
	}
	if project.OptionalDependencies == nil {
		project.OptionalDependencies = map[string]string{}
	}
	if project.DpmVersion == "" {
		project.DpmVersion = settings.DPM_VERSION.String()
	}

	if project.Slug == "" {
		project.Slug = utils.ToSlug(project.Name)
	}
	if project.Version == "" {
		project.Version = "0.1.0"
	}
	if project.License == "" {
		project.License = "GPL-3.0"
	}

	return project
}

func FixProjectJson() {
	project := utils.GetProjectJson()
	project = setProjectValues(project)
	project.DpmVersion = settings.DPM_VERSION.String()
	utils.SetProjectJson(project)
}

func makeMcmeta(versions []string, desc string) string {
	supportedFormats := make([]int, 0, len(versions))
	for _, version := range versions {
		supportedFormats = append(supportedFormats, utils.GetPackFormat(version))
	}

	return fmt.Sprintf(`{
  "pack": {
    "pack_format": %d,
    "description": "%s",
		"supported_fomats": [%d, %d]
  }
}`, slices.Max(supportedFormats), desc, slices.Min(supportedFormats), slices.Max(supportedFormats))
}

func makeTagFile(name string) string {
	return fmt.Sprintf(`{
  "values": [
    "%s"
  ]
}`, name)
}

func CreateTemplate(context types.Context) {
	template, name := context.Values[0], context.Values[1]

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

func createBasic(name string) types.Project {
	err := os.Mkdir(name, 0777)
	if err != nil {
		log.Fatal(err)
	}
	err = os.Chdir(name)
	if err != nil {
		log.Fatal(err)
	}

	project := CreateProject(types.Project{Name: name})
	namespace := utils.ToNamespace(name)
	mcmeta := makeMcmeta(project.GameVersions, fmt.Sprintf("%s v%s", project.Name, project.Version))

	os.WriteFile("pack.mcmeta", []byte(mcmeta), 0666)

	err = os.MkdirAll(path.Join("data", "minecraft", "tags", "functions"), 0777)
	if err != nil {
		log.Fatal(err)
	}

	writeFile(path.Join("data", "minecraft", "tags", "functions", "tick.json"), makeTagFile(namespace+":tick"))
	writeFile(path.Join("data", "minecraft", "tags", "functions", "load.json"), makeTagFile(namespace+":load"))

	err = os.MkdirAll(path.Join("data", namespace, "functions"), 0777)
	if err != nil {
		log.Fatal(err)
	}

	writeFile(path.Join("data", namespace, "functions", "load.mcfunction"), fmt.Sprintf(`tellraw @a "Loaded %s v%s"`, project.Name, project.Version))
	writeFile(path.Join("data", namespace, "functions", "tick.mcfunction"), "")

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

	namespace := utils.ToNamespace(name)

	writeFile(path.Join("data", namespace, "functions", "load.mcfunction"), fmt.Sprintf(LOAD_TEXT, namespace, namespace))
	writeFile(path.Join("data", namespace, "functions", "version.mcfunction"), fmt.Sprintf(VERSION_TEXT, namespace, project.Version, project.Name, namespace))
	writeFile(path.Join("data", namespace, "functions", "objectives.mcfunction"), "")
}
