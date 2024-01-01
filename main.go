package main

import (
	"fmt"
	"os"
)

// 0.1.2-indev-0
var DPM_VERSION = version{
	Major: 0,
	Minor: 1,
	Patch: 2,
	Extra: 0,
	Kind:  "indev",
}

func main() {
	args := parseArgs(os.Args[1:])

	var auth string

	authVal, ok := args.flags["auth"]

	if ok {
		auth = authVal[0]
	}

	aliases := getAliases()
	if alias, ok := aliases[auth]; ok {
		auth = alias
	}

	if _, ok := args.flags["help"]; ok {
		help(args.action)
		return
	}

	if _, ok := args.flags["version"]; ok {
		fmt.Printf("DPM v%s\n", DPM_VERSION.String())
		return
	}

	switch args.action {
	case "install":
		if _, ok := args.flags["dev"]; ok {
			install(args.data, auth, "dev")
		} else if _, ok := args.flags["optional"]; ok {
			install(args.data, auth, "optional")
		} else {
			install(args.data, auth, "")
		}
	case "uninstall":
		if _, ok := args.flags["dev"]; ok {
			uninstall(args.data, auth, "dev")
		} else if _, ok := args.flags["optional"]; ok {
			uninstall(args.data, auth, "optional")
		} else {
			uninstall(args.data, auth, "")
		}
	case "publish":
		publish(auth)
	case "init":
		initProject()
	case "fix":
		fixProjectJson()
	case "alias":
		createAlias(args.data[0], args.data[1])
	case "rm-alias":
		removeAlias(args.data[0])
	case "create":
		createTemplate(args.data[0], args.data[1])
	default:
		help("")
	}
}
