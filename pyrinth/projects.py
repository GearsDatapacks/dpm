import requests as r
import json


class Project:
    def __init__(self, project_model) -> None:
        if type(project_model) == dict:
            from pyrinth.models import ProjectModel
            project_model = ProjectModel.from_json(project_model)
        self.project_model = project_model

    def __repr__(self) -> str:
        return f"Project: {self.project_model.title}"

    def get_versions(self) -> list:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/version'
        )
        response = json.loads(raw_response.content)
        return [self.Version(version) for version in response]

    def check_validity(self) -> bool:
        """
        This function checks if a project exists

        Args:
            id (str): The id of the project

        Returns:
            bool: If the project exists
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.id}/check'
        )
        response = json.loads(raw_response.content)
        return (True if response['id'] else False)

    class Version:
        def __init__(self, version_model=None) -> None:
            if type(version_model) == dict:
                from pyrinth.models import VersionModel
                version_model = VersionModel.from_json(version_model)
                self.version_model = version_model
            self.version_model = version_model

        def __repr__(self) -> str:
            return f"Version: {self.version_model.name}"

    class VersionNumber:
        def __init__(self, major: int, minor: int, patch: int) -> None:
            self.major = major
            self.minor = minor
            self.patch = patch

        def __repr__(self) -> str:
            return f"v{self.major}.{self.minor}.{self.patch}"
