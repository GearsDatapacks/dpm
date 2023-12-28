package main

import (
	"fmt"
	"strings"
)

func help(action string) {
	actionData, ok := actions[action]

	if !ok {
		fmt.Println(helpText)
		return
	}

	aliasText := strings.Join(actionData.aliases, ", ")
	if aliasText != "" {
		fmt.Println(actionData.helpMessage + "\n\naliases: " + aliasText)
	} else {
		fmt.Println(actionData.helpMessage)
	}
}
