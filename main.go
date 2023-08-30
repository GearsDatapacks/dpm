package main

import (
	"fmt"
	"os"
)

const DPM_VERSION = "0.1.0-beta-1"

func main() {
	args := parseArgs(os.Args[1:])

	auth, ok := args.values["auth"]

	if !ok {
		auth = ""
	}

	if contains(args.flags, "help") {
		help(args.action)
		return
	}

	if contains(args.flags, "version") {
		fmt.Printf("DPM v%s\n", DPM_VERSION)
		return
	}

	if args.action == "install" {
		install(args.data, auth)
	} else if args.action == "publish" {
		publish(auth)
	} else if args.action == "init" {
		initProject()
	} else {
		help("")
	}
}
