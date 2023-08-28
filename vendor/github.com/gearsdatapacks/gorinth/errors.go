package gorinth

import (
	"fmt"
	"os"
)

func format(log string, logType string, values []any) string {
	return "[Gorinth] " + logType + " - " + fmt.Sprintf(log, values...)
}

func logError(err string, values ...any) {
	fmt.Println(format(err, "Error", values))
	os.Exit(1)
}

func logWarning(warn string, values ...any) {
	fmt.Println(format(warn, "Warning", values))
	os.Exit(1)
}

func logInfo(info string, values ...any) {
	fmt.Println(format(info, "Info", values))
	os.Exit(1)
}
