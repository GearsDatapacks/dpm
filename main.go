package main

import (
	"fmt"
	"os"
)

// 0.1.1-indev-0
var DPM_VERSION = version{
	Major: 0,
	Minor: 1,
	Patch: 0,
	Extra: 0,
	Kind: "indev",
}

func main() {
	args := parseArgs(os.Args[1:])

	auth, ok := args.values["auth"]

	if !ok {
		auth = ""
	}

	aliases := getAliases()
	if alias, ok := aliases[auth]; ok {
		auth = alias
	}

	if contains(args.flags, "help") {
		help(args.action)
		return
	}

	if contains(args.flags, "version") {
		fmt.Printf("DPM v%s\n", DPM_VERSION.String())
		return
	}

	if args.action == "install" {
		if contains(args.flags, "dev") {
			install(args.data, auth, "dev")
		} else if contains(args.flags, "optional") {
			install(args.data, auth, "optional")
		} else {
			install(args.data, auth, "")
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
