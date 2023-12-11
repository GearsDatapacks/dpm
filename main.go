package main

import (
	"fmt"
	"os"
)

// 0.1.0-rc-2
var DPM_VERSION = version{
	Major: 0,
	Minor: 1,
	Patch: 0,
	Extra: 2,
	Kind:  "rc",
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
		install(args.data, auth)
	} else if args.action == "publish" {
		publish(auth)
	} else if args.action == "init" {
		initProject()
	} else if args.action == "alias" {
		createAlias(args.data[0], args.data[1])
	} else if args.action == "create" {
		createTemplate(args.data[0], args.data[1])
	} else {
		help("")
	}
}
