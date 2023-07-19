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

	if args.action == "install" {
		install(args.data, auth)
	} else if args.action == "publish" {
		// Publish project
	} else if args.action == "init" {
		// Initialise project
	} else {
		log.Fatalf("Invalid action %q", args.action)
	}
}
