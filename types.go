package main

type projectJson struct {
	Name         string            `json:"name"`
	Slug         string            `json:"slug"`
	Version      string            `json:"version"`
	GameVersions []string          `json:"game_versions"`
	Summary      string            `json:"summary"`
	License      string            `json:"license"`
	Categories   []string          `json:"categories"`
	Dependencies map[string]string `json:"dependencies"`
	ReleaseType  string            `json:"release_type"`
}
