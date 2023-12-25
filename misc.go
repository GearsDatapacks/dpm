package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"
)

var aliasFile = joinPath(dpmDir, "aliases.json")

func createAlias(name string, auth string) {
	if _, err := os.ReadDir(dpmDir); err != nil {
		err := os.Mkdir(dpmDir, 0777)
		if err != nil {
			log.Fatal(err)
		}
	}

	if !exists(aliasFile) {
		_, err := os.Create(aliasFile)
		if err != nil {
			log.Fatal(err)
		}
	}

	contents, err := os.ReadFile(aliasFile)
	if err != nil {
		log.Fatal(err)
	}

	aliases := map[string]string{}
	json.Unmarshal(contents, &aliases)

	aliases[name] = auth

	setAliases(aliases)

	fmt.Printf("Created alias %q\n", name)
}

func removeAlias(name string) {
	if !exists(aliasFile) {
		fmt.Printf("Alias %q does not exist\n", name)
		return
	}
	aliases := getAliases()
	if _, ok := aliases[name]; !ok {
		fmt.Printf("Alias %q does not exist\n", name)
		return
	}
	fmt.Printf("Removed alias %q\n", name)
	delete(aliases, name)
	setAliases(aliases)
}

func getAliases() map[string]string {
	if !exists(aliasFile) {
		return map[string]string{}
	}

	contents, err := os.ReadFile(aliasFile)
	if err != nil {
		log.Fatal(err)
	}

	aliases := map[string]string{}
	err = json.Unmarshal(contents, &aliases)
	if err != nil {
		log.Fatal(err)
	}

	return aliases
}

func setAliases(aliases map[string]string) {
	newAliases, err := json.MarshalIndent(aliases, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(aliasFile, newAliases, 0666)
	if err != nil {
		log.Fatal(err)
	}
}
