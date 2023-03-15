import requests as r
import json


class Version:
    def __init__(self, version):
        self.id = version['id']
        self.project_id = version['project_id']
        self.author_id = version['author_id']
        self.featured = version['featured']
        self.name = version['name']
        self.version_number = version['version_number']
        self.changelog = version['changelog']
        self.changelog_url = version['changelog_url']
        self.date_published = version['date_published']
        self.downloads = version['downloads']
        self.version_type = version['version_type']
        self.status = version['status']
        self.requested_status = version['requested_status']
        self.files = version['files']
        self.dependencies = version['dependencies']
        self.game_versions = version['game_versions']
        self.loaders = version['loaders']


class Project:
    def __init__(self, project_data):
        self.data = project_data
        self.id = self.data['id']
        self.slug = self.data['slug']
        self.project_type = self.data['project_type']
        self.team = self.data['team']
        self.title = self.data['title']
        self.description = self.data['description']
        self.body = self.data['body']
        self.body_url = self.data['body_url']
        self.published = self.data['published']
        self.updated = self.data['updated']
        self.approved = self.data['approved']
        self.status = self.data['status']
        self.requested_status = self.data['requested_status']
        self.moderator_message = self.data['moderator_message']
        self.license = self.data['license']
        self.client_side = self.data['client_side']
        self.server_side = self.data['server_side']
        self.downloads = self.data['downloads']
        self.followers = self.data['followers']
        self.categories = self.data['categories']
        self.additional_categories = self.data['additional_categories']
        self.game_versions = self.data['game_versions']
        self.loaders = self.data['loaders']
        self.versions = self.data['versions']
        self.icon_url = self.data['icon_url']
        self.issues_url = self.data['issues_url']
        self.github_url = self.data['source_url']
        self.wiki_url = self.data['wiki_url']
        self.discord_url = self.data['discord_url']
        self.donation_urls = self.data['donation_urls']
        self.gallery = self.data['gallery']
        self.flame_anvil_project = self.data['flame_anvil_project']
        self.flame_anvil_user = self.data['flame_anvil_user']
        self.color = self.data['color']

    def get_versions(self):
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.id}/version'
        )
        response = json.loads(raw_response.content)
        print(response)


def get_project_dependencies(id) -> list[Project]:
    """This function gets project dependencies

    Args:
        id (str): The ID of the project

    Returns:
        list: The project dependencies
    """
    raw_response = r.get(
        f'https://api.modrinth.com/v2/project/{id}/dependencies'
    )
    response = json.loads(raw_response.content)
    return [Project(project) for project in response['projects']]


def check_project_validity(id) -> bool:
    """
    This function checks if a project exists

    Args:
        id (str): The id of the project

    Returns:
        bool: If the project exists
    """
    raw_response = r.get(
        f'https://api.modrinth.com/v2/project/{id}/check'
    )
    return raw_response.ok


def get_random_project(count=1) -> list[Project]:
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


def get_project_versions(id) -> list[Version]:
    raw_response = r.get(
        f'https://api.modrinth.com/v2/project/{id}/version'
    )
    response = json.loads(raw_response.content)
    return [Version(version) for version in response]


def get_version(id) -> Version:
    raw_response = r.get(
        f'https://api.modrinth.com/v2/version/{id}'
    )
    response = json.loads(raw_response.content)
    return Version(response)


def get_versions(ids) -> list[Version]:
    raw_response = r.get(
        f'https://api.modrinth.com/v2/versions',
        params={
            'ids': json.dumps(ids)
        }
    )
    response = json.loads(raw_response.content)
    return [Version(version) for version in response]
