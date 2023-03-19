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
    def __init__(self) -> None:
        raise Exception("This class cannot be initalized!")

    # Returns Project
    @staticmethod
    def get_project(id: str, auth: str = '') -> object:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}',
            headers={
                'authorization': auth
            }
        )
        if not raw_response.ok:
            return None
        response = json.loads(raw_response.content)
        return Project(response, auth)

    # Returns list[Project]
    @staticmethod
    def get_projects(ids: list[str]) -> list[object]:
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
        return [Project(project) for project in response]

    # Returns Project.Version
    @staticmethod
    def get_version(id: str) -> object:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id}'
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content}")
            return None
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
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content}")
            return None
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]

    # Returns User
    @staticmethod
    def get_user_from_id(id: str) -> object:
        return User.from_id(id)

    # Returns User
    @staticmethod
    def get_user_from_auth(auth: str) -> object:
        return User.from_id(auth)

    @staticmethod
    # Returns list[Modrinth.SearchResult]
    def search_projects(query: str = '', facets: list[list[str]] = [], index: str = "relevance", offset: int = 0, limit: int = 10, filters: int = []) -> list[object]:
        if query == '' and facets == [] and index == 'relevance' and offset == 0 and limit == 10 and filters == []:
            raise Exception("Please specify a parameter to search")
        params = {}
        if query != '':
            params.update({'query': query})
        if facets != []:
            params.update({'facets': json.dumps(facets)})
        if index != 'relevance':
            params.update({'index': index})
        if offset != 0:
            params.update({'offset': offset})
        if limit != 10:
            params.update({'limit': limit})
        if filters != []:
            params.update({'filters': json.dumps(filters)})
        raw_response = r.get(
            f'https://api.modrinth.com/v2/search',
            params=params
        )
        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content}")
            return None
        response = json.loads(raw_response.content)
        return [Modrinth.SearchResult(project) for project in response['hits']]

    class SearchResult:
        def __init__(self, search_result_model) -> None:
            from pyrinth.models import SearchResultModel
            if type(search_result_model) == dict:
                search_result_model = SearchResultModel.from_json(
                    search_result_model
                )
            self.search_result_model = search_result_model

        def __repr__(self) -> str:
            return f"Search Result: {self.search_result_model.title}"

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
