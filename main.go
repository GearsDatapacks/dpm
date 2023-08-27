package main

import (
	"log"
	"os"
)

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

	if args.action == "install" {
		install(args.data, auth)
	} else if args.action == "publish" {
		publish(auth)
	} else if args.action == "init" {
		initProject()
	} else {
		log.Fatalf("Invalid action %q", args.action)
	}
}
