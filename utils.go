package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"strings"
)

var reader = bufio.NewReader(os.Stdin)

func contains[T comparable](slice []T, element T) bool {
	for _, x := range slice {
		if x == element {
			return true
		}
	}

	return false
}

func exists(filename string) bool {
	_, err := os.Stat(filename)

	return err == nil
}

func isDir(filename string) bool {
	info, err := os.Stat(filename)
	if err != nil {
		log.Fatal(err)
	}

	return info.IsDir()
}

func prompt(prompt string) string {
	fmt.Print(prompt)
	result, err := reader.ReadString('\n')

	if err != nil {
		log.Fatal(err)
	}

	return strings.TrimSpace(result)
}

func toSlug(title string) string {
	lower := strings.ToLower(title)
	hyphenated := strings.ReplaceAll(lower, " ", "-")
	return hyphenated
}

func toNamespace(title string) string {
	return strings.ReplaceAll(toSlug(title), "-", "_")
}

func getProjectJson() projectJson {
	if !exists("project.json") {
		log.Fatal("Could not find project.json. Please run dpm init to initialise a project.")
	}

	projectBytes, err := os.ReadFile("project.json")

	if err != nil {
		log.Fatal(err)
	}

	project := projectJson{}
	err = json.Unmarshal(projectBytes, &project)

	if err != nil {
		log.Fatal(err)
	}

	return project
}

func setProjectJson(project projectJson) {
	bytes, err := json.MarshalIndent(project, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile("project.json", bytes, 0666)

	if err != nil {
		log.Fatal(err)
	}
}

func joinPath(names ...string) string {
	return strings.Join(names, pathSeparator)
}
