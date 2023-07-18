package main

import (
	"log"
	"os"
)

func main() {
	args := parseArgs(os.Args[1:])

	if args.action == "install" {
		// Install datapack
	} else if args.action == "publish" {
		// Publish project
	} else if args.action == "init" {
		// Initialise project
	} else {
		log.Fatalf("Invalid action %q", args.action)
	}
}
