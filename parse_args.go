package main

import (
	"log"
	"strings"
)

type parsedArgs struct {
	action string
	data []string
	flags []string
	values map[string]string
}

var flagArgs = []string{"help", "version"}
var valueArgs = []string{"auth"}
var aliasEntries = map[string][]string{
	"install": {"i"},
	"init": {"initialise", "initialize"},
}
var aliases = map[string]string{}

func formatAliases() {
	for command, aliasArray := range aliasEntries {
		for _, alias := range aliasArray {
			aliases[alias] = command
		}
	}
}

func parseArgs(args []string) parsedArgs {
	formatAliases()

	result := parsedArgs{
		values: map[string]string{},
	}

	for i := 0; i < len(args); i++ {
		arg := args[i]

		if alias, ok := aliases[arg]; ok {
			arg = alias
		}

		if arg == "install" {
			result.action = "install"
			result.data = []string{}

			for (i + 1) < len(args) && !strings.HasPrefix(args[i + 1], "-") {
				result.data = append(result.data, args[i + 1])
				i++
			}
		} else if arg == "publish" {
			result.action = "publish"
		} else if arg == "init" {
			result.action = "init"
		} else if arg == "alias" {
			result.action = "alias"
			result.data = []string{}

			if i + 2 >= len(args) {
				log.Fatal("Subcommand 'alias' takes two arguments")
			}

			result.data = append(result.data, args[i+1], args[i+2])

			i += 2
		} else if strings.HasPrefix(arg, "--") {
			argName := arg[2:]

			if contains(flagArgs, argName) {
				result.flags = append(result.flags, argName)
			} else if contains(valueArgs, argName) {
				i++
				result.values[argName] = args[i]
			} else {
				log.Fatalf("Unexpected argument %q", arg)
			}
		} else {
			log.Fatalf("Unexpected argument %q", arg)
		}
	}

	return result
}
