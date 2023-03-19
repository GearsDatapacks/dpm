import requests as r
import json
from pyrinth.util import remove_file_path, remove_null_values, json_to_query_params


class Project:
    def __init__(self, project_model, auth: str = '') -> None:
        from pyrinth.models import ProjectModel
        if type(project_model) == dict:
            from pyrinth.models import ProjectModel
            project_model = ProjectModel.from_json(project_model)
        self.project_model = project_model
        self.auth = auth

    def __repr__(self) -> str:
        return f"Project: {self.project_model.title}"

    def get_latest_version(self, loaders=None, game_versions=None, featured=None):
        versions = self.get_versions(loaders, game_versions, featured)
        if versions:
            return versions[0]
        
        return None

    def get_specific_version(self, schematic_versioning):
        versions = self.get_versions()
        if versions:
            for version in versions:
                if version.version_model.version_number == schematic_versioning:
                    return version
        return None

    def get_oldest_version(self, loaders=None, game_versions=None, featured=None):
        versions = self.get_versions(loaders, game_versions, featured)
        if versions:
            return versions[-1]
        
        return None
    
    def get_id(self):
        return self.project_model.id

    def get_versions(self, loaders=None, game_versions=None, featured=None) -> list:
        filters = {
            'loaders': loaders,
            'game_versions': game_versions,
            'featured': featured
        }

        filters = remove_null_values(filters)
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/version',
            params=json_to_query_params(filters),
            headers={
                'authorization': self.auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request : {raw_response.content} (get_versions)")
            return None
        
        response = json.loads(raw_response.content)
        if response == []:
            print("Project has no versions")
            return None
        
        return [self.Version(version) for version in response]

    def get_version(id: str) -> object:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/version/{id}'
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (get_version)")
            return None
        
        response = json.loads(raw_response.content)
        return Project.Version(response)

    def create_version(self, auth: str, version_model: object):
        version_model.project_id = self.project_model.id

        files = {
            "data": version_model.to_bytes()
        }

        # key = name
        # value = path
        for file in version_model.files:
            files.update({remove_file_path(file): open(file, "rb").read()})

        raw_response = r.post(
            f'https://api.modrinth.com/v2/version',
            headers={
                "Authorization": auth
            },
            files=files
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (create_version)")
            return None
        
        return 1

    def change_icon(self, file_path: str, auth: str) -> None:
        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/icon',
            
            params={
                "ext": file_path.split(".")[-1]
            },

            headers={
                "authorization": auth
            },

            data=open(file_path, "rb")
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (change_icon)")
            return None
        
        return 1

    def delete_icon(self, auth: str):
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/icon',
            headers={
                "authorization": auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (delete_icon)")
            return None
        
        return 1

    def add_gallery_image(self, auth: str, image):
        raw_response = r.post(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
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

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (add_gallery_image)")
            return None
        
        return 1

    def delete_gallery_image(self, url: str, auth: str):
        if '-raw' in url:
            raise Exception(
                "Please use cdn.modrinth.com instead of cdn-raw.modrinth.com"
            )
        
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
            headers={
                "authorization": auth
            },
            params={
                "url": url
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (delete_gallery_image)")
            return None
        
        return 1

    def exists(self) -> bool:
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/check'
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
        
        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}',
            data=json.dumps(modified_json),
            headers={
                'Content-Type': 'application/json',
                'authorization': auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (modify)")
            return None
        
        return 1

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
        
        raw_response = r.patch(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/gallery',
            params=modified_json,
            headers={
                'authorization': auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (modify_gallery_image)")
            return None
        
        return 1

    def delete(self, auth: str) -> None:
        raw_response = r.delete(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}',
            headers={
                'authorization': auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request: {raw_response.content} (delete)")
            return None
        
        return 1

    def get_dependencies(self, auth: str = ''):
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{self.project_model.slug}/dependencies',
            headers={
                'authorization': auth
            }
        )

        if not raw_response.ok:
            print(f"Invalid Request : {raw_response.content} (get_dependencies)")
            return None
        
        response = json.loads(raw_response.content)
        return [Project(dependency) for dependency in response['projects']]

    class Version:
        def __init__(self, version_model=None) -> None:
            if type(version_model) == dict:
                from pyrinth.models import VersionModel
                version_model = VersionModel.from_json(version_model)
                self.version_model = version_model
            self.version_model = version_model

        def get_dependencies(self):
            return self.version_model.dependencies
        
        def get_files(self):
            result = []
            for file in self.version_model.files:
                result.append(Project.File.from_json(file))
            return result

        def __repr__(self) -> str:
            return f"Version: {self.version_model.name}"

    class GalleryImage:
        def __init__(self, file_path: str, featured: bool, title: str = '', description: str = '', ordering: int = 0) -> None:
            self.file_path = file_path
            self.ext = file_path.split(".")[-1]
            self.featured = str(featured).lower()
            self.title = title
            self.description = description
            self.ordering = ordering

        def from_json(json):
            result = Project.GalleryImage(
                json['url'], json['featured'], json['title'],
                json['description'], json['ordering']
            )

            return result

    class File:
        def __init__(self, hashes, url, filename, primary, size, file_type):
            self.hashes = hashes
            self.url = url
            self.filename = filename
            self.primary = primary
            self.size = size
            self.file_type = file_type
            self.extension = filename.split('.')[-1]

        def from_json(json):
            result = Project.File(
                json['hashes'],
                json['url'],
                json['filename'],
                json['primary'],
                json['size'],
                json['file_type']
            )
            return result

        def __repr__(self) -> str:
            return f"File: {self.filename}"

    class License:
        def __init__(self, id, name, url):
            self.id = id
            self.name = name
            self.url = url

        def from_json(json):
            result = Project.License(
                json['id'],
                json['name'],
                json['url']
            )

            return result

        def __repr__(self):
            return f"License: {self.name if self.name else self.id}"

    class Donation:
        def __init__(self, id, platform, url):
            self.id = id
            self.platform = platform
            self.url = url

        def from_json(json):
            print('JSON: ' + str(json))
            result = Project.Donation(
                json['id'],
                json['platform'],
                json['url']
            )

            return result

        def __repr__(self) -> str:
            return f"Donation: {self.platform}"
