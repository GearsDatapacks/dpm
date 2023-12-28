package main

var actions = map[string]action{
	"install": {
		argCount:    -1,
		aliases:     []string{"i"},
		helpMessage: installText,
	},
	"uninstall": {
		argCount:    -1,
		aliases:     []string{"remove", "ui"},
		helpMessage: uninstallText,
	},
	"publish": {
		argCount:    0,
		helpMessage: publishText,
	},
	"init": {
		argCount:    0,
		aliases:     []string{"initialise", "initialize"},
		helpMessage: initText,
	},
	"alias": {
		argCount:    2,
		helpMessage: aliasText,
	},
	"create": {
		argCount:    2,
		helpMessage: createText,
	},
	"rm-alias": {
		argCount:    1,
		helpMessage: rmAliasText,
	},
}

var flags = map[string]int{
	"help":     0,
	"version":  0,
	"dev":      0,
	"optional": 0,
	"auth":     1,
}

var aliases = formatAliases(actions)

func formatAliases(actions map[string]action) map[string]string {
	aliases := map[string]string{}
	for command, action := range actions {
		if action.aliases == nil {
			continue
		}
		for _, alias := range action.aliases {
			aliases[alias] = command
		}
	}
	return aliases
}

const installText = `Add specified datapacks as dependencies

Usage:
dpm install code-of-copper item-utils
dpm install

If left blank, it will download all dependencies of te current project

You can specify the version of the dependency using the following syntax:
dpm install moxlib@0.5.5
The above code installs moxlib version 0.5.5.

By default, if you do not specify the version, it will download the latest stable release. You can override this behaviour like so:
dpm install code-of-copper@latest
That downloads the most recent version, regardless of release type.

If --dev is passed, it will instead store the projects as dev dependencies (Or download dev dependencies, if left blank). Dev dependencies are libraries only used in development, and are not published to Modrinth.

If --optional is passed, it will instead store the projects as optional dependencies (Or download optional dependencies, if left blank). Optional dependencies are marked as optional on Modrinth, and not automatically downloaded.`

const uninstallText = `Removes specified datapacks from dependencies

Usage:
dpm uninstall code-of-copper item-utils
dpm uninstall moxlib --dev

If --dev is passed, it will instead remove the project from dev dependencies.

If --optional is passed, it will instead remove the project from optional dependencies.`

const publishText = `Publish your DPM project to Modrinth (requires --auth)

Usage:
dpm publish --auth foo

Zips up your datapack files and uses the infromation in the project.json file to create a version for the datapack on Modrinth`

const initText = `Initialise a DPM project

Usage:
dpm init

Creates a project.json file with information about your datapack`

var aliasText = `Create an auth alias

Usage:
dpm alias gears bar && dpm publish --auth gears

Stores the auth token in ` + aliasFile + ` and replaces the name with the token when used`

const createText = `Remove an auth alias

Usage:
dpm rm-alias gears

Removes the given alias from the registry`

const rmAliasText = `Generate a datapack from a template

Usage:
dpm create <template-name> <project-name>

Templates:
basic: The minimum required files for a datapack
simple: Some useful files created`

const helpText = `Usage: dpm <action> [options]
Actions:
init                                    Initialise a DPM project
install <datapacks>                     Add datapacks as dependencies
install                                 Download all dependencies
uninstall <datapacks>                   Remove datapacks from dependencies
publish                                 Publish your DPM project to Modrinth (requires --auth)
alias <name> <auth>                     Create an auth alias
rm-alias <name>                         Removes an auth alias
create <template-name> <project-name>   Generate a datapack from a template

Options:
--auth <auth>      Specify a Modrinth authorisation token
--help             Show information on a specific DPM command
--version          Output current DPM version
--dev              Install a dev dependency
--optional         Install an optional dependency

For more information on specific actions, run dpm <action> --help`
