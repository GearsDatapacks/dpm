package main

import (
	"fmt"
	"os"

	"github.com/gearsdatapacks/dpm/alias"
	"github.com/gearsdatapacks/dpm/args"
	"github.com/gearsdatapacks/dpm/modrinth"
	"github.com/gearsdatapacks/dpm/project"
	"github.com/gearsdatapacks/dpm/settings"
	"github.com/gearsdatapacks/dpm/types"
)

func main() {
	arguments := args.ParseArgs(os.Args[1:])

	var auth string

	authVal, ok := arguments.Flags["auth"]

	if ok {
		auth = authVal[0]
	}

	aliases := alias.GetAliases()
	if alias, ok := aliases[auth]; ok {
		auth = alias
	}

	if _, ok := arguments.Flags["help"]; ok {
		args.Help(arguments.Action)
		return
	}

	if _, ok := arguments.Flags["version"]; ok {
		fmt.Printf("DPM v%s\n", settings.DPM_VERSION.String())
		return
	}

	context := types.Context{
		Auth: auth,
	}

	switch arguments.Action {
	case "install":
		if _, ok := arguments.Flags["dev"]; ok {
			modrinth.Install(context, "dev")
		} else if _, ok := arguments.Flags["optional"]; ok {
			modrinth.Install(context, "optional")
		} else {
			modrinth.Install(context, "")
		}
	case "uninstall":
		if _, ok := arguments.Flags["dev"]; ok {
			modrinth.Uninstall(context, "dev")
		} else if _, ok := arguments.Flags["optional"]; ok {
			modrinth.Uninstall(context, "optional")
		} else {
			modrinth.Uninstall(context, "")
		}

	case "publish":
		modrinth.Publish(auth)
	case "init":
		project.InitProject()
	case "fix":
		project.FixProjectJson()
	case "alias":
		alias.CreateAlias(context)
	case "rm-alias":
		alias.RemoveAlias(context)
	case "create":
		project.CreateTemplate(context)
	case "fetch":
		modrinth.Fetch(context)
	default:
		args.Help("")
	}
}
