import json
import requests as r


class Statistics:
    def __init__(self, statistics):
        self.authors = statistics['authors']
        self.files = statistics['files']
        self.projects = statistics['projects']
        self.versions = statistics['versions']


def get_modrinth_stats() -> Statistics:
    raw_response = r.get(
        f'https://api.modrinth.com/v2/statistics'
    )
    response = json.loads(raw_response.content)
    return Statistics(response)
