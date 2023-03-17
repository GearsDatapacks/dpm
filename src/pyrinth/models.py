from pyrinth.projects import *
from pyrinth.util import *
import json


class ProjectModel:
    def __init__(
        self, slug: str, title: str,
        description: str, categories: list[str],
        client_side: str, server_side: str, body: str,
        license_id: str, project_type: str,
        additional_categories: list[str] = None,
        issues_url: str = None, source_url: str = None,
        wiki_url: str = None, discord_url: str = None,
        donation_urls: list[Project.Donation] = None,
        license_url: str = None
    ) -> None:
        self.slug = slug
        self.title = title
        self.description = description
        self.categories = categories
        self.client_side = client_side
        self.server_side = server_side
        self.body = body
        self.license_id = Project.License(
            license_id['id'], license_id['name'], license_id['url']
        ) if type(license_id) == dict else license_id
        self.project_type = project_type
        self.additional_categories = additional_categories
        self.issues_url = issues_url
        self.source_url = source_url
        self.wiki_url = wiki_url
        self.discord_url = discord_url
        self.donation_urls = [Project.Donation(
            donation_url['id'],
            donation_url['platform'],
            donation_url['url']
        ) for donation_url in donation_urls]
        self.license_url = license_url
        self.id = None
        self.downloads = None

    def from_json(json):
        result = ProjectModel(
            json['slug'], json['title'], json['description'],
            json['categories'], json['client_side'], json['server_side'],
            json['body'], json['license'], json['project_type'],
            json['additional_categories'], json['issues_url'], json['source_url'],
            json['wiki_url'], json['discord_url'], json['donation_urls'],
            json['license']['url']
        )
        result.id = json['id']
        result.downloads = json['downloads']
        return result

    def to_json(self):
        result = {
            'slug': self.slug,
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
            'id': self.id,
            'is_draft': True,
            'initial_versions': []
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self):
        return json.dumps(self.to_json()).encode()


class SearchResultModel:
    # Commented out because I figure that you dont need to initalize this class. But I might be wrong...

    # def __init__(self, slug: str, title: str, description: str, client_side: str, server_side: str, project_type: str, downloads: int, project_id: str, author: str, versions: list[str], follows: int, date_created, date_modified, license, categories: list[str], icon_url: None, color: None, display_categories: list[str], latest_version: str, gallery: list[str], featured_gallery: None) -> None:
    # def __init__(self) -> None:
    #     self.slug = slug
    #     self.title = title
    #     self.description = description
    #     self.client_side = client_side
    #     self.server_side = server_side
    #     self.project_type = project_type
    #     self.downloads = downloads
    #     self.project_id = project_id
    #     self.author = author
    #     self.versions = versions
    #     self.follows = follows
    #     self.date_created = date_created
    #     self.date_modified = date_modified
    #     self.license = license
    #     self.categories = categories
    #     self.icon_url = icon_url
    #     self.color = color
    #     self.display_categories = display_categories
    #     self.latest_version = latest_version
    #     self.gallery = gallery
    #     self.featured_gallery = featured_gallery

    def from_json(json):
        result = SearchResultModel()
        result.slug = json['slug']
        result.title = json['title']
        result.description = json['description']
        result.client_side = json['client_side']
        result.server_side = json['server_side']
        result.project_type = json['project_type']
        result.downloads = json['downloads']
        result.project_id = json['project_id']
        result.author = json['author']
        result.versions = json['versions']
        result.follows = json['follows']
        result.date_created = json['date_created']
        result.date_modified = json['date_modified']
        result.license = json['license']
        result.categories = json['categories']
        result.icon_url = json['icon_url']
        result.color = json['color']
        result.display_categories = json['display_categories']
        result.latest_version = json['latest_version']
        result.gallery = json['gallery']
        result.featured_gallery = json['featured_gallery']

        return result

    # def to_json(self):
    #     result = {
    #         'slug': self.slug,
    #         'title': self.title,
    #         'description': self.description,
    #         'client_side': self.client_side,
    #         'server_side': self.server_side,
    #         'project_type': self.project_type,
    #         'downloads': self.downloads,
    #         'project_id': self.project_id,
    #         'author': self.author,
    #         'versions': self.versions,
    #         'follows': self.follows,
    #         'date_created': self.date_created,
    #         'date_modified': self.date_modified,
    #         'license': self.license,
    #         'categories': self.categories,
    #         'icon_url': self.icon_url,
    #         'color': self.color,
    #         'display_categories': self.display_categories,
    #         'latest_version': self.latest_version,
    #         'gallery': self.gallery,
    #         'featured_gallery': self.featured_gallery
    #     }
    #     result = remove_null_values(result)
    #     return result

    # def to_bytes(self):
    #     return json.dumps(self.to_json()).encode()


class VersionModel:
    def __init__(
        self, title, version_number, dependencies, game_versions, version_type, loaders, featured, files, changelog=None, status=None, requested_status=None, main_file=None, project_id=None
    ):
        self.title = title
        self.version_number = version_number
        self.changelog = changelog
        self.dependencies = dependencies
        self.game_versions = game_versions
        self.version_type = version_type
        self.loaders = loaders
        self.featured = featured
        self.status = status
        self.requested_status = requested_status
        self.file_parts = files
        self.primary_file = main_file
        self.project_id = project_id

    def from_json(json_):
        primary_files = []
        for primary_files_ in json_['files']:
            if primary_files_['primary']:
                primary_files.append(primary_files_)
        result = VersionModel(
            json_['name'], json_['version_number'], json_['changelog'],
            json_['dependencies'], json_[
                'game_versions'], json_['version_type'],
            json_['loaders'], json_['featured'], json_['status'],
            json_['requested_status'], json_[
                'files'], primary_files,
            json_['project_id']
        )
        return result

    def to_json(self):
        result = {
            'name': self.title,
            'version_number': self.version_number,
            'changelog': self.changelog,
            'dependencies': self.dependencies,
            'game_versions': self.game_versions,
            'version_type': self.version_type,
            'loaders': self.loaders,
            'featured': self.featured,
            'status': self.status,
            'requested_status': self.requested_status,
            'file_parts': self.files,
            'primary_file': self.primary_file,
            'project_id': self.project_id
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self):
        return json.dumps(self.to_json()).encode()


class UserModel:
    def __init__(
        self, username, id, avatar_url, created, role, name=None, email=None, bio=None, payout_data=None, github_id=None, badges=None
    ):
        self.username = username
        self.id = id
        self.avatar_url = avatar_url
        self.created = created
        self.role = role
        self.name = name
        self.email = email
        self.bio = bio
        self.payout_data = payout_data
        self.github_id = github_id
        self.badges = badges

    def from_json(json):
        result = VersionModel(
            json['username'], json['id'], json['avatar_url'],
            json['created'], json['role'], json['name'],
            json['email'], json['bio'], json['payout_data'],
            json['github_id'], json['badges']
        )
        return result

    def to_json(self):
        result = {
            'username': self.username,
            'id': self.id,
            'avatar_url': self.avatar_url,
            'created': self.created,
            'role': self.role,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'payout_data': self.payout_data,
            'github_id': self.github_id,
            'badges': self.badges
        }
        result = remove_null_values(result)
        return result

    def to_bytes(self):
        return json.dumps(self.to_json()).encode()


class TeamMemberModel:
    ...
