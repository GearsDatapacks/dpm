package gorinth

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
)

func GetUserFromAuth(auth string) User {
	body, status := get("https://api.modrinth.com/v2/user", authHeader(auth))

	if status == 401 {
		logError("Invalid authorisation token given")
	}

	if status == 200 {
		user := User{}

		err := json.Unmarshal(body, &user)
		if err != nil {
			logError(err.Error())
		}
		user.auth = auth

		return user
	}

	logError("Unexpected response status %d", status)

	return User{}
}

func (user User) CreateProject(project Project) error {
	project.Validate()
	overriddenValues := removeNullValues(project)

	overriddenValues["license_id"] = project.License.Id

	parts := map[string]io.Reader{}

	if project.Icon != nil {
		parts = map[string]io.Reader{"icon": bytes.NewBuffer(project.Icon)}
	}

	body, status := post(
		"https://api.modrinth.com/v2/project",
		overriddenValues,
		authHeader(user.auth),
		parts,
	)

	if status == 200 {
		return nil
	}

	if status == 400 {
		return fmt.Errorf("invalid request when attempting to create project %q: %s", project.Title, string(body))
	}

	if status == 401 {
		return fmt.Errorf("no authorisation to create project %q", project.Title)
	}

	return fmt.Errorf("unexpected status code %d", status)
}
