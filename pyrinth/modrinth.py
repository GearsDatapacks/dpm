import requests as r
import json
from pyrinth.models import SearchResultModel
from pyrinth.projects import Project
from pyrinth.users import User


class SearchResult:
    def __init__(self, search_result_model) -> None:
        if type(search_result_model) == dict:
            search_result_model = SearchResultModel.from_json(
                search_result_model
            )
        self.search_result_model = search_result_model

    def __repr__(self) -> str:
        return f"Search Result: {self.search_result_model.title}"


class Modrinth:
    def __init__(self):
        raise Exception("This class cannot be initalized!")

    @staticmethod
    def get_project(id: str, auth: str = '') -> Project:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}',
            headers={
                'authorization': auth
            }
        )
        if raw_response.status_code == 404:
            raise Exception(
                "The requested project was not found or no authorization to see this project."
            )
        response = json.loads(raw_response.content)
        return Project(response)

    @staticmethod
    def get_projects(ids: list[str] = []) -> list[Project]:
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
    def get_version(id: str) -> Project.Version:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id}'
        )
        response = json.loads(raw_response.content)
        return Project.Version(response)

    @staticmethod
    def get_random_projects(count: int = 1) -> list:
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

    @staticmethod
    def search_projects(query='', facets=[], index="relevance", offset=0, limit=10, filters=[]) -> list[SearchResult]:
        print("[INFO] SEARCH PROJECTS IS NOT FULLY IMPLEMENTED YET")
        raw_response = r.get(
            f'https://api.modrinth.com/v2/search',
            params={
                'query': query,
                # 'facets': facets,
                'index': index,
                'offset': offset,
                'limit': limit,
                # 'filters': filters
            }
        )
        response = json.loads(raw_response.content)
        return [SearchResult(project) for project in response['hits']]

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
