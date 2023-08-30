//go:build !windows

package main

import "os"

var homeDir, _ = os.UserHomeDir()
var dpmDir = homeDir + "/.local/share/dpm"
var aliasFile = dpmDir + "/aliases.json"
