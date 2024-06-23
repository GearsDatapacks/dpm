package utils

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path"
	"strings"

	"github.com/gearsdatapacks/dpm/settings"
	"github.com/gearsdatapacks/dpm/types"
)

var reader = bufio.NewReader(os.Stdin)

var AliasFile = path.Join(settings.DpmDir, "aliases.json")

func Exists(filename string) bool {
	_, err := os.Stat(filename)

	return err == nil
}

func IsDir(filename string) bool {
	info, err := os.Stat(filename)
	if err != nil {
		log.Fatal(err)
	}

	return info.IsDir()
}

func Prompt(prompt string) string {
	fmt.Print(prompt)
	result, err := reader.ReadString('\n')

	if err != nil {
		log.Fatal(err)
	}

	return strings.TrimSpace(result)
}

func ToSlug(title string) string {
	lower := strings.ToLower(title)
	hyphenated := strings.ReplaceAll(lower, " ", "-")
	return hyphenated
}

func ToNamespace(title string) string {
	return strings.ReplaceAll(ToSlug(title), "-", "_")
}

func GetConfig() (types.Config, bool) {
	if !Exists("dpmconfig.json") {
		return types.Config{}, false
	}

	projectBytes, err := os.ReadFile("dpmconfig.json")

	if err != nil {
		return types.Config{}, false
	}

	config := types.Config{}
	err = json.Unmarshal(projectBytes, &config)

	if err != nil {
		return types.Config{}, false
	}

	return config, true
}

func GetProjectJson() types.Project {
	if !Exists("project.json") {
		log.Fatal("Could not find project.json. Please run dpm init to initialise a project.")
	}

	projectBytes, err := os.ReadFile("project.json")

	if err != nil {
		log.Fatal(err)
	}

	project := types.Project{}
	err = json.Unmarshal(projectBytes, &project)

	if err != nil {
		log.Fatal(err)
	}

	return project
}

func SetProjectJson(project types.Project) {
	bytes, err := json.MarshalIndent(project, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("project.json", bytes, 0666)

	if err != nil {
		log.Fatal(err)
	}
}

var cacheFile = path.Join(settings.DpmDir, "cache.json")

func GetCache() types.Cache {
	if Exists(cacheFile) {
		bytes, err := os.ReadFile(cacheFile)

		if err != nil {
			log.Fatal(err)
		}

		cache := types.Cache{}
		err = json.Unmarshal(bytes, &cache)

		if err != nil {
			log.Fatal(err)
		}

		return cache
	}

	return types.Cache{
		PackFormats: map[string]int{},
	}
}

func SetCache(cache types.Cache) {
	bytes, err := json.MarshalIndent(cache, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(cacheFile, bytes, 0666)

	if err != nil {
		log.Fatal(err)
	}
}
