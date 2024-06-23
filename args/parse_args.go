package args

import (
	"log"
	"strings"
)

type ParsedArgs struct {
	Action string
	Data   []string
	Flags  map[string][]string
}

type action struct {
	ArgCount    int
	HelpMessage string
	Aliases     []string
}

func ParseArgs(args []string) ParsedArgs {
	result := ParsedArgs{
		Flags: map[string][]string{},
	}

	for i := 0; i < len(args); i++ {
		arg := args[i]

		if alias, ok := Aliases[arg]; ok {
			arg = alias
		}

		if strings.HasPrefix(arg, "--") {
			argName := arg[2:]
			argCount, ok := flags[argName]

			if !ok {
				log.Fatalf("Unexpected argument %q", arg)
			}
			result.Flags[argName] = []string{}
			for count := 0; count < argCount; count++ {
				i++
				if i >= len(args) || strings.HasPrefix(args[i], "--") {
					log.Fatalf("Flag %q takes %d arguments", arg, argCount)
				}
				result.Flags[argName] = append(result.Flags[argName], args[i])
			}

			continue
		}

		action, ok := Actions[arg]
		if !ok {
			log.Fatalf("Unexpected argument %q", arg)
		}

		if result.Action != "" {
			log.Fatalf("Unexpected argument %q", arg)
		}
		result.Action = arg
		result.Data = []string{}
		argCount := action.ArgCount

		if argCount == 0 {
			continue
		}

		if argCount == -1 {
			for (i+1) < len(args) && !strings.HasPrefix(args[i+1], "--") {
				result.Data = append(result.Data, args[i+1])
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
			result.Data = append(result.Data, args[i])
		}
		continue
	}
	return result
}

func (p *ParsedArgs) FlagValue(flag string) string {
	if value, ok := p.Flags[flag]; ok {
		return value[0]
	}
	return ""
}

func (p *ParsedArgs) HasFlag(flag string) bool {
	_, ok := p.Flags[flag]
	return ok
}
