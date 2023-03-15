import json
import requests as r


class ModrinthStatistics:
    def __init__(self):
        raw_response = r.get(
            f'https://api.modrinth.com/v2/statistics'
        )
        response = json.loads(raw_response.content)
        self.authors = response['authors']
        self.files = response['files']
        self.projects = response['projects']
        self.versions = response['versions']
