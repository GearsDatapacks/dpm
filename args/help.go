package args

import (
	"fmt"
	"strings"
)

func Help(action string) {
	actionData, ok := Actions[action]

	if !ok {
		fmt.Println(HelpText)
		return
	}

	aliasText := strings.Join(actionData.Aliases, ", ")
	if aliasText != "" {
		fmt.Println(actionData.HelpMessage + "\n\naliases: " + aliasText)
	} else {
		fmt.Println(actionData.HelpMessage)
	}
}
