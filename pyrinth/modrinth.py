import requests as r
import json
from pyrinth.projects import Project
from pyrinth.users import User


class Modrinth:
    @staticmethod
    def get_project(id: str) -> Project:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}'
        )
        response = json.loads(raw_response.content)
        return Project(response)

    @staticmethod
    def get_projects_by_ids(ids: list[str] = []) -> list[Project]:
        """This function finds multiple projects by IDs, then returns them

        Args:
            ids (list[str]): the IDs of the projects

        Returns:
            list[Project]: The projects that were searched using ids
        """
        if ids == []:
            raise Exception(
                "Please specify project IDs to get project details. Or use this method on an instanced class"
            )
        raw_response = r.get(
            f'https://api.modrinth.com/v2/projects',
            params={
                'ids': json.dumps(ids)
            }
        )
        response = json.loads(raw_response.content)
        if not raw_response.ok:
            raise Exception(
                response['description'] + " Did you supply a project slug instead of a ID?")
        return [Project(project) for project in response]

    @staticmethod
    def get_version_by_id(id: str) -> Project.Version:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id}'
        )
        response = json.loads(raw_response.content)
        return Project.Version(response)

    @staticmethod
    def get_random_project(count: int = 1) -> list:
        """This function returns a random project

        Args:
            count (int, optional): Amount of random projects to return. Defaults to 1.

        Returns:
            list[Project]: The random projects
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/projects_random',
            params={
                'count': count
            }
        )
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    @staticmethod
    def get_user_from_id(id: str) -> User:
        return User.from_id(id)

    @staticmethod
    def get_user_from_auth(auth: str) -> User:
        return User.from_id(auth)

    class Statistics:
        def __init__(self) -> None:
            raw_response = r.get(
                f'https://api.modrinth.com/v2/statistics'
            )
            response = json.loads(raw_response.content)
            self.authors = response['authors']
            self.files = response['files']
            self.projects = response['projects']
            self.versions = response['versions']