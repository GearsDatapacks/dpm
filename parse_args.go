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

type action struct {
	argCount int
	helpMessage string
	aliases []string
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

		action, ok := actions[arg]
		if !ok {
			log.Fatalf("Unexpected argument %q", arg)
		}

		if result.action != "" {
			log.Fatalf("Unexpected argument %q", arg)
		}
		result.action = arg
		result.data = []string{}
		argCount := action.argCount

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
