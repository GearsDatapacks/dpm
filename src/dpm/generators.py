import json
import os
from util import *

def init(dir):
    if os.path.exists(f"{dir}/project.json"):
        print('File project.json already exists.')
        return

    title = input("Title of project: ")
    slug = input(f"Project slug ({to_slug(title)}): ") or to_slug(title)
    version = input("Current version (0.1.0): ") or "0.1.0"
    game_versions = input("Enter space separated compatible game versions: ").split(" ")
    summary = input("Summary of datapack: ")
    license = input("Project license (GPL): ") or "GPL-3.0"

    project_json = {
        "name": title,
        "slug": slug,
        "version": version,
        "game_versions": game_versions,
        "summary": summary,
        "description": "",
        "license": license,
        "categories": [],
        "dependencies": {},
        "release_type": "release"
    }

    with open(f"{dir}/project.json", "w") as f:
        f.write(json.dumps(project_json, indent=2))
  