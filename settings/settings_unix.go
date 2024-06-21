//go:build !windows

package settings

import "os"

const PathSeparator = "/"

var homeDir, _ = os.UserHomeDir()
var DpmDir = homeDir + "/.local/share/dpm"
