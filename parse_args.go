package main

import (
	"log"
	"strings"
)

type parsedArgs struct {
	action string
	data   []string
	flags map[string][]string
}

var actions = map[string]int{
	"install":   -1,
	"uninstall": -1,
	"publish":   0,
	"init":      0,
	"alias":     2,
	"create":    2,
	"rm-alias":  1,
}
var flags = map[string]int{
	"help":     0,
	"version":  0,
	"dev":      0,
	"optional": 0,
	"auth":     1,
}
var aliasEntries = map[string][]string{
	"uninstall": {"remove", "ui"},
	"install":   {"i"},
	"init":      {"initialise", "initialize"},
}
var aliases = formatAliases(aliasEntries)

func formatAliases(unformatted map[string][]string) map[string]string {
	aliases := map[string]string{}
	for command, aliasArray := range unformatted {
		for _, alias := range aliasArray {
			aliases[alias] = command
		}
	}
	return aliases
}

func parseArgs(args []string) parsedArgs {
	result := parsedArgs{
		flags: map[string][]string{},
	}

	for i := 0; i < len(args); i++ {
		arg := args[i]

		if alias, ok := aliases[arg]; ok {
			arg = alias
		}

		if strings.HasPrefix(arg, "--") {
			argName := arg[2:]
			argCount, ok := flags[argName]

			if !ok {
				log.Fatalf("Unexpected argument %q", arg)
			}
			result.flags[argName] = []string{}
			for count := 0; count < argCount; count++ {
				i++
				if i >= len(args) || strings.HasPrefix(args[i], "--") {
					log.Fatalf("Flag %q takes %d arguments", arg, argCount)
				}
				result.flags[argName] = append(result.flags[argName], args[i])
			}

			continue
		}

		argCount, ok := actions[arg]
		if !ok {
			log.Fatalf("Unexpected argument %q", arg)
		}

		if result.action != "" {
			log.Fatalf("Unexpected argument %q", arg)
		}
		result.action = arg
		result.data = []string{}

		if argCount == 0 {
			continue
		}

		if argCount == -1 {
			for (i+1) < len(args) && !strings.HasPrefix(args[i+1], "--") {
				result.data = append(result.data, args[i+1])
				i++
			}
			continue
		}

		if (i+1) < len(args) && strings.HasPrefix(args[i+1], "--") {
			continue
		}

		for count := 0; count < argCount; count++ {
			i++
			if i >= len(args) || strings.HasPrefix(args[i], "--") {
				log.Fatalf("Subcommand %q takes %d arguments", arg, argCount)
			}
			result.data = append(result.data, args[i])
		}
		continue
	}
	return result
}
