package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

var reader = bufio.NewReader(os.Stdin)

func contains[T comparable] (slice []T, element T) bool {
	for _, x := range slice {
		if x == element {
			return true
		}
	}

	return false
}

func exists(filename string) bool {
	_, err := os.Stat(filename)

	return err == nil
}

func prompt(prompt string) string {
	fmt.Print(prompt)
	result, err := reader.ReadString('\n')

	if err != nil {
		log.Fatal(err)
	}

	return strings.TrimSpace(result)
}

func toSlug(title string) string {
	lower := strings.ToLower(title)
	hyphenated := strings.ReplaceAll(lower, " ", "-")
	return hyphenated
}
