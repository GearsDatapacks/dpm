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
        donation_urls=None, license_url=None, id=None
    ) -> None:
        self.slug = slug
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
        self.id = id

    def from_json(json):
        result = ProjectModel(
            json['slug'], json['title'], json['description'],
            json['categories'], json['client_side'], json['server_side'],
            json['body'], json['license'], json['project_type'],
            json['additional_categories'], json['issues_url'], json['source_url'],
            json['wiki_url'], json['discord_url'], json['donation_urls'],
            json['license']['url'], json['id']
        )
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


class DependencyModel:
    def __init__(self, id, slug, project_type, team, title, description, body, body_url, published, updated, approved, status, requested_status, moderator_message, license, client_side, server_side, downloads, followers, categories, additional_categories, game_versions, loaders, versions, icon_url, issues_url, source_url, wiki_url, discord_url, donation_urls, gallery, flame_anvil_project, flame_anvil_user, color):
        self.id = id
        self.slug = slug
        self.project_type = project_type
        self.team = team
        self.title = title
        self.description = description
        self.body = body
        self.body_url = body_url
        self.published = published
        self.updated = updated
        self.approved = approved
        self.status = status
        self.requested_status = requested_status
        self.moderator_message = moderator_message
        self.license = license
        self.client_side = client_side
        self.server_side = server_side
        self.downloads = downloads
        self.followers = followers
        self.categories = categories
        self.additional_categories = additional_categories
        self.game_versions = game_versions
        self.loaders = loaders
        self.versions = versions
        self.icon_url = icon_url
        self.issues_url = issues_url
        self.source_url = source_url
        self.wiki_url = wiki_url
        self.discord_url = discord_url
        self.donation_urls = donation_urls
        self.gallery = to_image_from_json(gallery)
        self.flame_anvil_project = flame_anvil_project
        self.flame_anvil_user = flame_anvil_user
        self.color = color

    def from_json(json):
        result = DependencyModel(
            json['id'], json['slug'], json['project_type'],
            json['team'], json['title'], json['description'],
            json['body'], json['body_url'], json['published'],
            json['updated'], json['approved'], json['status'],
            json['requested_status'], json['moderator_message'], json['license'],
            json['client_side'], json['server_side'], json['downloads'],
            json['followers'], json['categories'], json['additional_categories'],
            json['game_versions'], json['loaders'], json['versions'],
            json['icon_url'], json['issues_url'], json['source_url'],
            json['wiki_url'], json['discord_url'], json['donation_urls'],
            json['gallery'], json['flame_anvil_project'], json['flame_anvil_user'],
            json['color']
        )
        return result

    def to_json(self):
        result = {
            'id': self.id,
            'slug': self.slug,
            'project_type': self.project_type,
            'team': self.team,
            'title': self.title,
            'description': self.description,
            'body': self.body,
            'body_url': self.body_url,
            'published': self.published,
            'updated': self.updated,
            'approved': self.approved,
            'status': self.status,
            'requested_status': self.requested_status,
            'moderator_message': self.moderator_message,
            'license': self.license,
            'client_side': self.client_side,
            'server_side': self.server_side,
            'downloads': self.downloads,
            'followers': self.followers,
            'categories': self.categories,
            'additional_categories': self.additional_categories,
            'game_versions': self.game_versions,
            'loaders': self.loaders,
            'versions': self.versions,
            'icon_url': self.icon_url,
            'issues_url': self.issues_url,
            'source_url': self.source_url,
            'wiki_url': self.wiki_url,
            'discord_url': self.discord_url,
            'donation_urls': self.donation_urls,
            'gallery': self.gallery,
            'flame_anvil_project': self.flame_anvil_project,
            'flame_anvil_user': self.flame_anvil_user,
            'color': self.color
        }
        result = remove_null_values(result)

        return result


class SearchResultModel:
    def __init__(self, slug: str, title: str, description: str, client_side: str, server_side: str, project_type: str, downloads: int, project_id: str, author: str, versions: list[str], follows: int, date_created, date_modified, license, categories: list[str], icon_url: None, color: None, display_categories: list[str], latest_version: str, gallery: list[str], featured_gallery: None) -> None:
        ...
        self.slug = slug
        self.title = title
        self.description = description
        self.client_side = client_side
        self.server_side = server_side
        self.project_type = project_type
        self.downloads = downloads
        self.project_id = project_id
        self.author = author
        self.versions = versions
        self.follows = follows
        self.date_created = date_created
        self.date_modified = date_modified
        self.license = license
        self.categories = categories
        self.icon_url = icon_url
        self.color = color
        self.display_categories = display_categories
        self.latest_version = latest_version
        self.gallery = gallery
        self.featured_gallery = featured_gallery

    def from_json(json):
        result = SearchResultModel(
            json["slug"], json["title"], json["description"],
            json["client_side"], json["server_side"], json["project_type"],
            json["downloads"], json["project_id"], json["author"],
            json["versions"], json["follows"], json["date_created"],
            json["date_modified"], json["license"], json["categories"],
            json["icon_url"], json["color"], json["display_categories"],
            json["latest_version"], json["gallery"], json["featured_gallery"]
        )

        return result

    def to_json(self):
        result = {
            'slug': self.slug,
            'title': self.title,
            'description': self.description,
            'client_side': self.client_side,
            'server_side': self.server_side,
            'project_type': self.project_type,
            'downloads': self.downloads,
            'project_id': self.project_id,
            'author': self.author,
            'versions': self.versions,
            'follows': self.follows,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'license': self.license,
            'categories': self.categories,
            'icon_url': self.icon_url,
            'color': self.color,
            'display_categories': self.display_categories,
            'latest_version': self.latest_version,
            'gallery': self.gallery,
            'featured_gallery': self.featured_gallery
        }
        result = remove_null_values(result)
        return result


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
            'file_parts': self.file_parts,
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


class TeamMemberModel:
    ...
