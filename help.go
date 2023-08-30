package main

import (
	"fmt"
	"log"
)

func help(action string) {
	if action == "" {
		fmt.Println(
`Usage: dpm <action> [options]
Actions:
init                            Initialise a DPM project
install <datapacks>             Add datapacks as dependencies
install                         Download all dependencies
publish                         Publish your DPM project to Modrinth (requires --auth)
alias <name> <auth>             Create an auth alias

Options:
--auth <auth>      Specify a Modrinth authorisation token
--help             Show information on a specific DPM command`)
		return
	}

	if action == "init"{
    fmt.Println(
`Initialise a DPM project

Usage:
dpm init

Creates a project.json file with information about your datapack

aliases: initialise, initialize`)
		return
	}

  if action == "install" {
     fmt.Println(
`Add specified datapacks as dependencies

Usage:
dpm install code-of-copper item-utils
dpm install

If left blank, it will download all dependencies of te current project

aliases: i`)
		return
	}

  if action == "publish"{
    fmt.Println(
`Publish your DPM project to Modrinth (requires --auth)

Usage:
dpm publish --auth foo

Zips up your datapack files and uses the infromation in the project.json file to create a version for the datapack on Modrinth`)
		return
	}

	if action == "alias"{
    fmt.Println(
`Create an auth alias

Usage:
dpm alias gears bar && dpm publish --auth gears

Stores the auth token in ` + aliasFile + ` and replaces the name with the token when used`)
		return
	}

  log.Fatalf("Unexpected action %q", action)
}
