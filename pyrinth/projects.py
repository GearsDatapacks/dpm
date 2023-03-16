import requests as r
import json
from pyrinth.util import *


class Project:
    def __init__(self, project_model) -> None:
        if type(project_model) == dict:
            from pyrinth.models import ProjectModel
            project_model = ProjectModel.from_json(project_model)
        self.project_model = project_model

    def __repr__(self) -> str:
        return f"Project: {self.project_model.title}"

    def get_versions(self, loaders=None, game_versions=None, featured=None) -> list:
        filters = {
            'loaders': loaders,
            'game_versions': game_versions,
            'featured': featured
        }
        filters = remove_null_values(filters)
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/version',
            params=json_to_query_params(filters)
        )
        print(raw_response.url)
        response = json.loads(raw_response.content)
        return [self.Version(version) for version in response]

    def change_icon(self, file_path: str, auth: str) -> None:
        r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/icon',
            params={
                "ext": file_path.split(".")[-1]
            },
            headers={
                "authorization": auth
            },
            data=open(file_path, "rb")
        )

    def delete_icon(self, auth: str):
        r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/icon',
            headers={
                "authorization": auth
            }
        )

    def add_gallery_image(self, auth: str, image):
        r.post(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/gallery',
            headers={
                "authorization": auth
            },
            params={
                "ext": image.ext,
                "featured": image.featured,
                "title": image.title,
                "description": image.description,
                "ordering": image.ordering
            },
            data=open(image.file_path, "rb")
        )

    def delete_gallery_image(self, url: str, auth: str):
        if '-raw' in url:
            raise Exception(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/gallery',
            headers={
                "authorization": auth
            },
            params={
                "url": url
            }
        )

        print(raw_response.content)

    def exists(self) -> bool:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/check'
        )
        response = json.loads(raw_response.content)
        return (True if response['id'] else False)

    def modify(self, auth, slug=None, title=None, description=None, categories=None, client_side=None, server_side=None, body=None, additional_categories=None, issues_url=None, source_url=None, wiki_url=None, discord_url=None, donation_urls=None, license_id=None, license_url=None, status=None, requested_status=None, moderation_message=None, moderation_message_body=None):

        modified_json = {
            'slug': slug,
            'title': title,
            'description': description,
            'categories': categories,
            'client_side': client_side,
            'server_side': server_side,
            'body': body,
            'additional_categories': additional_categories,
            'issues_url': issues_url,
            'source_url': source_url,
            'wiki_url': wiki_url,
            'discord_url': discord_url,
            'donation_urls': donation_urls,
            'license_id': license_id,
            'license_url': license_url,
            'status': status,
            'requested_status': requested_status,
            'moderation_message': moderation_message,
            'moderation_message_body': moderation_message_body
        }
        modified_json = remove_null_values(modified_json)
        if not modified_json:
            raise Exception("Please specify at least 1 optional argument.")
        r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}',
            data=json.dumps(modified_json),
            headers={
                'Content-Type': 'application/json',
                'authorization': auth
            }
        )

    def modify_gallery_image(self, auth, url, featured=None, title=None, description=None, ordering=None):
        modified_json = {
            'url': url,
            'featured': featured,
            'title': title,
            'description': description,
            'ordering': ordering
        }
        modified_json = remove_null_values(modified_json)
        if not modified_json:
            raise Exception("Please specify at least 1 optional argument.")
        r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/gallery',
            params=modified_json,
            headers={
                'authorization': auth
            }
        )

    def delete(self, auth: str) -> None:
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}',
            headers={
                'authorization': auth
            }
        )
        if raw_response.status_code == 400:
            raise Exception("The requested project was not found.")
        elif raw_response.status_code == 401:
            raise Exception("Invalid authorization token.")

    def get_dependencies(self, auth: str = ''):
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.id}/dependencies',
            headers={
                'authorization': auth
            }
        )
        response = json.loads(raw_response.content)
        from pyrinth.projects import Project
        return [Project.Dependency(dependency) for dependency in response['projects']]

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

    class GalleryImage:
        def __init__(self, file_path: str, extension: str, featured: bool, title: str = '', description: str = '', ordering: int = 0) -> None:
            self.file_path = file_path
            self.ext = extension
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

    class Dependency:
        def __init__(self, dependency_model) -> None:
            from pyrinth.models import DependencyModel
            if type(dependency_model) == dict:
                dependency_model = DependencyModel.from_json(
                    dependency_model
                )
            self.dependency_model = dependency_model

        def __repr__(self) -> str:
            return f"Dependency: {self.dependency_model.title}"
