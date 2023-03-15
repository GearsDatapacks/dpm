import requests as r
import json


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
        return [self.Version(version) for version in response]

    class Version:

        def __init__(
            self, version={}, version_model=None
        ):
            if version:
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

        # def from_args(
        #         name, version_number, dependencies,
        #         game_versions, version_type, loaders,
        #         featured, requested_status, project_id,
        #         file_parts, primary_file="primary_file", changelog="",
        #         status="unknown"
        # ):
        #     return Version(json.dumps({
        #         'name': name,
        #         'version_number': version_number,
        #         'changelog': changelog,
        #         'dependencies': dependencies,
        #         'game_versions': game_versions,
        #         'version_type': version_type,
        #         'loaders': loaders,
        #         'featured': featured,
        #         'status': status,
        #         'requested_status': requested_status,
        #         'project_id': project_id,
        #         'file_parts': file_parts,
        #         'primary_file': primary_file
        #     }))

    def get_dependencies(self=None, id=''):
        """This function gets project dependencies

        Args:
            id (str): The ID of the project

        Returns:
            list: The project dependencies
        """
        if id == '' and self == None:
            raise Exception(
                "Please specify a project ID to find dependencies. Or use this method on an instanced class"
            )
        id = self.id if not id else id
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}/dependencies'
        )
        response = json.loads(raw_response.content)
        return [Project(project) for project in response['projects']]

    def check_validity(self=None, id='') -> bool:
        """
        This function checks if a project exists

        Args:
            id (str): The id of the project

        Returns:
            bool: If the project exists
        """
        if id == '' and self == None:
            raise Exception(
                "Please specify a project ID to check validity. Or use this method on an instanced class"
            )
        id = self.id if not id else id
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}/check'
        )
        response = json.loads(raw_response.content)
        return (True if response['id'] else False)

    def get_random_project(count=1) -> list:
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

    def get_versions(self=None, id='') -> list:
        """This function gets a projects versions by ID

        Args:
            id (str, required if not using a instanced class): The ID of the project.

        Returns:
            list: The versions for the project
        """
        if id == '' and self == None:
            raise Exception(
                "Please specify a project ID to get project versions. Or use this method on an instanced class"
            )
        id = self.id if not id else id
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}/version'
        )
        response = json.loads(raw_response.content)
        return [self.Version(version) for version in response]

    def get_version(id) -> Version:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id}'
        )
        response = json.loads(raw_response.content)
        return Project.Version(response)
