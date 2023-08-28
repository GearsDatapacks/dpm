package gorinth

import (
	"encoding/json"
	"fmt"
)

func GetVersion(versionId string, auth string) Version {
	url := fmt.Sprintf("https://api.modrinth.com/v2/version/%s", versionId)
	result, statusCode := get(url, authHeader(auth))

	if statusCode == 404 {
		logError("Version %q wasn't found or no authorization to see this project", versionId)
	}

	version := Version{}

	json.Unmarshal(result, &version)

	return version
}
