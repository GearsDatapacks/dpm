//go:build windows

package main

import "os"

const pathSeparator = "\\"
var homeDir, _ = os.UserHomeDir()
var dpmDir = homeDir + "\\AppData\\dpm"
