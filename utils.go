package main

import (
	"os"
)

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
