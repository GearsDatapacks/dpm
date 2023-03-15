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

    def __repr__(self) -> str:
        return f"Project: {self.title}"

    def get_versions(self):
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.id}/version'
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

    def get_versions(self) -> list:
        """This function gets a projects versions by ID

        Args:
            id (str, required if not using a instanced class): The ID of the project.

        Returns:
            list: The versions for the project
        """
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.id}/version'
        )
        response = json.loads(raw_response.content)
        return [self.Version(version) for version in response]

    class Version:
        def __init__(self, version_model=None, version_dict=None):
            if not version_model and not version_dict:
                raise Exception(
                    "Please specify a version_model or a version_dict"
                )
            if version_dict:
                self.id = version_dict['id']
                self.project_id = version_dict['project_id']
                self.author_id = version_dict['author_id']
                self.featured = version_dict['featured']
                self.name = version_dict['name']
                self.version_number = version_dict['version_number']
                self.changelog = version_dict['changelog']
                self.changelog_url = version_dict['changelog_url']
                self.date_published = version_dict['date_published']
                self.downloads = version_dict['downloads']
                self.version_type = version_dict['version_type']
                self.status = version_dict['status']
                self.requested_status = version_dict['requested_status']
                self.files = version_dict['files']
                self.dependencies = version_dict['dependencies']
                self.game_versions = version_dict['game_versions']
                self.loaders = version_dict['loaders']
            if version_model:
                self.id = version_model.id
                self.project_id = version_model.project_id
                self.author_id = version_model.author_id
                self.featured = version_model.featured
                self.name = version_model.name
                self.version_number = version_model.version_number
                self.changelog = version_model.changelog
                self.changelog_url = version_model.changelog_url
                self.date_published = version_model.date_published
                self.downloads = version_model.downloads
                self.version_type = version_model.version_type
                self.status = version_model.status
                self.requested_status = version_model.requested_status
                self.files = version_model.files
                self.dependencies = version_model.dependencies
                self.game_versions = version_model.game_versions
                self.loaders = version_model.loaders

        def __repr__(self) -> str:
            return f"Version: {self.name}"
