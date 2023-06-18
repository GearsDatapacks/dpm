import json
import os
import sys
import shutil
from zipfile import ZipFile
from util import *
# TURN OFF YOUR FORMATTER, IT WILL PUT THIS IN THE WRONG ORDER AND IT WILL STOP WORKING!!!
import sys
# sys.path.append(f"C:/Users/{os.getlogin()}/OneDrive/Desktop/Pyrinth/src") # Testing - Windows
sys.path.append(f"../") # Testing - Other OS's
from pyrinth.modrinth import *
from pyrinth.models import *
from pyrinth.users import *
from pyrinth.projects import *

def create_project(namespace):
    namespace = to_slug(namespace)
    name = to_sentence_case(namespace)
    description = input(f"Enter the description of datapack '{name}': ")
    if len(description) < 3:
        print(f"Warning! You will not be able to publish '{name}' to modrinth if the description is under 3 characters!")
    if name == '':
        print("Datapack name cannot be blank")
        return
    tags_functions = f"{name}/data/minecraft/tags/functions"
    functions = f"{name}/data/{namespace}/functions"
    if not os.path.exists(tags_functions):
        os.makedirs(tags_functions)

    if not os.path.exists(functions):
        os.makedirs(functions)

    if not os.path.exists(f"{functions}/tick.mcfunction"):
        open(f"{functions}/tick.mcfunction", "x").close()

    if not os.path.exists(f"{tags_functions}/tick.json"):
        open(f"{tags_functions}/tick.json",
             "x").write(to_tags_json(namespace, "tick"))

    if not os.path.exists(f"{functions}/load.mcfunction"):
        open(f"{functions}/load.mcfunction", "x").close()

    if not os.path.exists(f"{tags_functions}/load.json"):
        open(f"{tags_functions}/load.json",
             "x").write(to_tags_json(namespace, "load"))

    if not os.path.exists(f"{name}/pack.mcmeta"):
        open(f"{name}/pack.mcmeta", "x").write(to_mcmeta_json(description))

    if not os.path.exists(f"{name}/project.json"):
        open(f"{name}/project.json",
             "x").write(to_project_json(name, namespace, description))
        
def publish_project(dir, auth):
    if not os.path.exists(f"{dir}/project.json"):
        print(f"Could not find project.json. Please initialise a project to publish")
        return

    with open(f"{dir}/project.json", "r") as f:
        project = json.loads(f.read())

    slug = project['slug'] or to_slug(project['name'])
    title = project['name']
    description = project['summary']
    body = project['description']
    categories = project['categories']
    license = project['license']
    version_number = project['version']

    modrinth_project: Project = Project.get(slug, auth)

    user = User.get_from_auth(auth)

    if modrinth_project:
      versions = modrinth_project.get_versions() or []

      has_version = False

      for version in versions:
          if version.version_model.version_number == version_number:
              has_version = True
              break

      modrinth_project.modify(auth=auth, title=title, description=description, body=body,  categories=categories, client_side='optional', server_side='required', license_id=license)

      if not has_version:
        publish_version(project, dir, auth)
    
    else:
      project = user.create_project(ProjectModel(
          slug, title, description, categories,
          'optional', 'required', body,
          license, 'mod'
      ))
      if project:
          print(f"Successfully published project '{title}'")
        
def publish_version(metadata, dir, auth):
    slug = metadata['slug']
    title = metadata['name']
    version_number = metadata['version']
    game_versions = metadata['game_versions']
    version_type = metadata['release_type']
    dependencies = format_dependencies(metadata["dependencies"])

    version_title = f"{title}-v{version_number}"

    zip_path = f"{dir}/{version_title}.zip"

    files_to_zip = ["data", "pack.mcmeta"]

    if os.path.exists(f"{dir}/pack.png"):
          files_to_zip.append("pack.png")

    for file in files_to_zip:
        if os.path.isdir(f"{dir}/{file}"):
          shutil.copytree(f"{dir}/{file}", file)
        else:
            shutil.copy(f"{dir}/{file}", file)
        
      
    with ZipFile(zip_path, "w") as zip_file:
        zip_file.write("data")
        zip_file.write("pack.mcmeta")
        if os.path.exists("pack.png"):
          zip_file.write("pack.png")

    for file in files_to_zip:
        if os.path.isdir(file):
          shutil.rmtree(file)
        else:
          os.remove(file)

    project = Project.get(slug, auth)

    if not project:
        print(f"Project '{title}' with slug '{slug}' was not found")
        return

    version = project.create_version(VersionModel(
        name=version_title, version_number=version_number, dependencies=dependencies,
        game_versions=game_versions, version_type=version_type, loaders=['datapack'],
        featured=True, file_parts=[zip_path]
    ), auth)

    if version:
        print(f"Successfully created version '{version_title}'")

def format_dependencies(dependencies):
    result = []

    dependency_array = list(dependencies.items())

    for dependency in dependency_array:
        slug = dependency[0]
        version_number = dependency[1]

        dependency_project = Project.get(slug)
        dependency_version = dependency_project.get_specific_version(version_number)
        formatted = {
            "project_id": dependency_project.project_model.id,
            "version_id": dependency_version.version_model.id,
            "dependency_type": "required"
        }

        result.append(formatted)
    
    return result

