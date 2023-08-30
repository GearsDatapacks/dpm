//go:build windows

package main

import "os"

var homeDir, _ = os.UserHomeDir()
var dpmDir = homeDir + "\\AppData\\dpm"
var aliasFile = dpmDir + "\\aliases.json"
