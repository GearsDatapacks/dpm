from pyrinth.projects import *
from pyrinth.util import *
import json


class ProjectModel:
    def __init__(
        self, slug: str, title: str,
        description: str, categories: list[str], client_side: str,
        server_side: str, body: str, license_id: str,
        project_type: str, additional_categories=None, issues_url=None,
        source_url=None, wiki_url=None, discord_url=None,
        donation_urls=None, license_url=None
    ) -> None:
        self.id = slug
        self.title = title
        self.description = description
        self.categories = categories
        self.client_side = client_side
        self.server_side = server_side
        self.body = body
        self.license_id = license_id
        self.project_type = project_type
        self.additional_categories = additional_categories
        self.issues_url = issues_url
        self.source_url = source_url
        self.wiki_url = wiki_url
        self.discord_url = discord_url
        self.donation_urls = donation_urls
        self.license_url = license_url

    def from_json(json):
        result = ProjectModel(
            json['slug'], json['title'], json['description'],
            json['categories'], json['client_side'], json['server_side'],
            json['body'], json['license'], json['project_type'],
            json['additional_categories'], json['issues_url'], json['source_url'],
            json['wiki_url'], json['discord_url'], json['donation_urls'],
            json['license']['url']
        )
        return result

    def to_json(self):
        result = {
            'slug': self.id,
            'title': self.title,
            'description': self.description,
            'categories': self.categories,
            'client_side': self.client_side,
            'server_side': self.server_side,
            'body': self.body,
            'license_id': self.license_id,
            'project_type': self.project_type,
            'additional_categories': self.additional_categories,
            'issues_url': self.issues_url,
            'source_url': self.source_url,
            'wiki_url': self.wiki_url,
            'discord_url': self.discord_url,
            'donation_urls': self.donation_urls,
            'license_url': self.license_url,
            'is_draft': True,
            'initial_versions': []
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self):
        # print(self.to_json())
        return json.dumps(self.to_json()).encode()


class SearchResultModel:
    ...


class VersionModel:
    def __init__(
        self, name: str, version_number: Project.VersionNumber, game_versions: list[str], version_type: str, loaders: list[str], featured: bool, id: str, project_id: str, author_id: str, date_published: str, downloads: int, files,
        changelog: str = None, dependencies: list = None, status: str = None, requested_status: str = None
    ):
        self.name = name
        self.version_number = version_number
        self.game_versions = game_versions
        self.version_type = version_type
        self.loaders = loaders
        self.featured = featured
        self.id = id
        self.project_id = project_id
        self.author_id = author_id
        self.date_published = date_published
        self.downloads = downloads
        self.files = files
        self.changelog = changelog
        self.dependencies = dependencies
        self.status = status
        self.requested_status = requested_status

    def from_json(json):
        result = VersionModel(
            json['name'], json['version_number'], json['game_versions'],
            json['version_type'], json['loaders'], json['featured'],
            json['id'], json['project_id'], json['author_id'],
            json['date_published'], json['downloads'], json['files'],
            json['changelog'], json['dependencies'], json['status'],
            json['requested_status']
        )
        return result

    def to_json(self):
        result = {
            'name': self.name,
            'version_number': self.version_number,
            'game_versions': self.game_versions,
            'version_type': self.version_type,
            'loaders': self.loaders,
            'featured': self.featured,
            'id': self.id,
            'project_id': self.project_id,
            'author_id': self.author_id,
            'date_published': self.date_published,
            'downloads': self.downloads,
            'files': self.files,
            'changelog': self.changelog,
            'dependencies': self.dependencies,
            'status': self.status,
            'requested_status': self.requested_status
        }
        return result


class UserModel:
    ...


class TeamMemberModel:
    ...
