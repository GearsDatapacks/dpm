package main

import (
	"fmt"
	"log"
	"strconv"
	"strings"
)

type projectJson struct {
	Name                 string            `json:"name"`
	Slug                 string            `json:"slug"`
	Version              string            `json:"version"`
	GameVersions         []string          `json:"game_versions"`
	Summary              string            `json:"summary"`
	License              string            `json:"license"`
	Categories           []string          `json:"categories"`
	AdditionalCategories []string          `json:"additional_categories"`
	Dependencies         map[string]string `json:"dependencies"`
	DevDependencies      map[string]string `json:"dev_dependencies"`
	OptionalDependencies map[string]string `json:"optional_dependencies"`
	ReleaseType          string            `json:"release_type"`
	DpmVersion           string            `json:"dpm_version"`
}

type version struct {
	Major uint64
	Minor uint64
	Patch uint64
	Extra uint64
	Kind  string
}

func (v *version) Greater(other version) bool {
	return v.Major > other.Major ||
		v.Minor > other.Minor ||
		v.Patch > other.Patch ||
		v.Extra > other.Extra
}

func (v *version) Less(other version) bool {
	return v.Major < other.Major ||
		v.Minor < other.Minor ||
		v.Patch < other.Patch ||
		v.Extra < other.Extra
}

func (v *version) String() string {
	if v.Kind == "" {
		return fmt.Sprintf("%d.%d.%d", v.Major, v.Minor, v.Patch)
	}
	return fmt.Sprintf("%d.%d.%d-%s-%d", v.Major, v.Minor, v.Patch, v.Kind, v.Extra)
}

func ParseVersion(input string) version {
	bits := strings.Split(input, "-")
	parts := strings.Split(bits[0], ".")
	if len(parts) < 3 {
		log.Fatal("Invalid version string")
	}
	ver := version{}

	var err error
	ver.Major, err = strconv.ParseUint(parts[0], 10, 32)
	if err != nil {
		log.Fatal("Invalid version string")
	}

	ver.Minor, err = strconv.ParseUint(parts[1], 10, 32)
	if err != nil {
		log.Fatal("Invalid version string")
	}

	ver.Patch, err = strconv.ParseUint(parts[2], 10, 32)
	if err != nil {
		log.Fatal("Invalid version string")
	}

	if len(bits) == 3 {
		ver.Kind = bits[1]
		ver.Extra, err = strconv.ParseUint(bits[2], 10, 32)
		if err != nil {
			log.Fatal("Invalid version string")
		}
	}

	return ver
}

type dpmConfig struct {
	IncludeFiles []string `json:"include_files"`
	ExcludeFiles []string `json:"exclude_files"`
}
