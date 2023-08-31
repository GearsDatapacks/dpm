package main

import (
	"encoding/json"
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

	newAliases, err := json.MarshalIndent(aliases, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	err = os.WriteFile(aliasFile, newAliases, 0666)
	if err != nil {
		log.Fatal(err)
	}
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
