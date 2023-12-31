package main

import (
	"fmt"
	"os"
)

// 0.1.1
var DPM_VERSION = version{
	Major: 0,
	Minor: 1,
	Patch: 1,
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

	if args.action == "install" {
		if _, ok := args.flags["dev"]; ok {
			install(args.data, auth, "dev")
		} else if _, ok := args.flags["optional"]; ok {
			install(args.data, auth, "optional")
		} else {
			install(args.data, auth, "")
		}
	} else if args.action == "uninstall" {
		if _, ok := args.flags["dev"]; ok {
			uninstall(args.data, auth, "dev")
		} else if _, ok := args.flags["optional"]; ok {
			uninstall(args.data, auth, "optional")
		} else {
			uninstall(args.data, auth, "")
		}
	} else if args.action == "publish" {
		publish(auth)
	} else if args.action == "init" {
		initProject()
	} else if args.action == "alias" {
		createAlias(args.data[0], args.data[1])
	} else if args.action == "rm-alias" {
		removeAlias(args.data[0])
	} else if args.action == "create" {
		createTemplate(args.data[0], args.data[1])
	} else {
		help("")
	}
}
