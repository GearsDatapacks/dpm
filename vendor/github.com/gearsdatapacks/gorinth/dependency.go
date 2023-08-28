package gorinth

func (dep Dependency) GetVersion() Version {
	if dep.VersionId == "" {
		project, err := GetProject(dep.ProjectId, "")

		if err != nil {
			logError(err.Error())
		}

		return project.GetLatestVersion()
	}

	return GetVersion(dep.VersionId, "")
}
