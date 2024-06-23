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

	auth := arguments.FlagValue("auth")
	noModify := arguments.FlagValue("no-modify")

	aliases := alias.GetAliases()
	if alias, ok := aliases[auth]; ok {
		auth = alias
	}

	if arguments.HasFlag("help") {
		args.Help(arguments.Action)
		return
	}

	if arguments.HasFlag("version") {
		fmt.Printf("DPM v%s\n", settings.DPM_VERSION.String())
		return
	}

	context := types.Context{
		Auth:   auth,
		Values: arguments.Data,
		Flags: types.ContextFlags{
			ModifyProject: noModify != "project",
			ModifyVersion: noModify != "version",
		},
	}

	switch arguments.Action {
	case "install":
		if arguments.HasFlag("dev") {
			modrinth.Install(context, "dev")
		} else if arguments.HasFlag("optional") {
			modrinth.Install(context, "optional")
		} else {
			modrinth.Install(context, "")
		}
	case "uninstall":
		if arguments.HasFlag("dev") {
			modrinth.Uninstall(context, "dev")
		} else if arguments.HasFlag("optional") {
			modrinth.Uninstall(context, "optional")
		} else {
			modrinth.Uninstall(context, "")
		}

	case "publish":
		modrinth.Publish(context)
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
