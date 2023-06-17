from help import dpm_help
from parse_args import parse_args
import json
from zipfile import ZipFile
import shutil
import webbrowser
import requests as r
import os
import sys
import time
from util import *
# TURN OFF YOUR FORMATTER, IT WILL PUT THIS IN THE WRONG ORDER AND IT WILL STOP WORKING!!!
import sys
# sys.path.append(f"C:/Users/{os.getlogin()}/OneDrive/Desktop/Pyrinth/src") # Testing - Windows
sys.path.append(f"../") # Testing - Other OS's
from pyrinth.modrinth import *
from pyrinth.models import *
from pyrinth.users import *
from pyrinth.projects import *
# -------------------


def download_file(file, dir,):

    # Create the full file path by joining the folder path and file name
    path = f"{dir}/{file.name}"

    # If the download was skipped
    if os.path.exists(path):
        print(
            f"{file.name.ljust(3, ' ')} already downloaded... skipping"
        )
        return 1

    # Send a GET request to the specified file URL and stream the response
    response = r.get(file.url, stream=True)

    # Get the total size of the file from the response headers
    total_progress = int(response.headers.get('content-length', 0))

    # Set the block size for reading data from the response
    block_size = 1024


    # Keep track of how much data has been downloaded
    progress = 0

    with open(path, 'wb') as f:
        start_time = time.perf_counter()

        # Iterate over the response data in chunks
        for data in response.iter_content(block_size):

            # Update the progress and write the data to the file
            progress += len(data)
            f.write(data)

            # Calculate and format the percentage of data that has been downloaded
            percent = progress / total_progress * 100
            percent = f'{percent:.2f}%'

            # Calculate and format the progress bar
            bar_length = progress / total_progress * 20
            bar_filled = '='*int(bar_length)
            bar_empty = ' '*(20-len(bar_filled))
            bar = bar_filled + bar_empty
            
            # Print the progress bar and percentage on the same line,
            # moving the cursor back to the beginning of the line using '\r'
            filename = file.name.ljust(3, ' ')
            print(
                f'Downloading {filename} [{bar}] / {percent}',
                end='\r'
            )

    end_time = time.perf_counter()
    time_taken = '{:.2f}'.format(end_time - start_time)

    print(
      f'Downloading {filename} [{bar}] / Done in {time_taken}s',
      end='\r'
    )

    print(f"\n", end='')

    return 0

def install(projects, dir, auth):
    download_dir = dir

    if os.path.exists(f'{dir}/project.json'):
        download_dir = f'{dir}/..'

    if len(projects) == 0:
      download_dependencies(dir, auth)
      return

    for project in projects:
        download_project(project, download_dir, auth)
        if os.path.exists(f'{dir}/project.json'):
          add_dependency(project, dir, auth)
          
def add_dependency(dependency, dir, auth):
  with open(f"{dir}/project.json", "r") as f:
    project = json.loads(f.read())
  
  
  dependency_project = Project.get(dependency, auth)
  latest_version = dependency_project.get_latest_version().version_model.version_number

  if not project["dependencies"]:
      project["dependencies"] = {}

  project["dependencies"][dependency] = latest_version

  with open(f"{dir}/project.json", "w") as f:
      f.write(json.dumps(project, indent=2))

def download_project(project_id, dir, auth=''):
    
    project = Project.get(project_id, auth)
    
    # If no project is found, print an error message and return None
    if not project:
        return None
    
    print(f"Project '{to_sentence_case(project.slug)}' found")

    # Get the latest version of the project and its files
    latest = project.get_latest_version(loaders=["datapack"])

    if not latest:
        return None
    
    project_files = latest.files
    
    # Get the dependencies of the project
    dependencies = project.dependencies
    
    # Initialize an empty list to keep track of all files that need to be downloaded
    downloading_versions = [latest]

    # If there are any dependencies, add their latest versions' files to the downloading_files list
    if dependencies:
        for dependency in dependencies:
            downloading_versions.append(
                dependency.get_latest_version()
            )

    # Keep track of how much time has taken to download all files
    # Keep track of how many files are skipped
    downloaded_files = 0

    start_time = time.perf_counter()

    for version in downloading_versions:
        downloaded_files += download_version(version, dir)
    
    end_time = time.perf_counter()
    time_taken = end_time - start_time

    if downloaded_files != 0:
        print(f"{downloaded_files} file(s) downloaded in {time_taken:.2f}s")
    else:
        print("Download no extra files")
    option = input("Would you like to open the projects modrinth page (y/N)? ").lower()
    if option == "y" or option == "yes":
        webbrowser.open(
            f"https://modrinth.com/datapack/{project.project_model.id}"
        )

def download_dependencies(dir, auth):
  with open(f"{dir}/project.json", "r") as f:
     project = json.loads(f.read())
  
  dependencies = project["dependencies"].items()

  for dependency in dependencies:
    slug = dependency[0]
    semantic_version = dependency[1]

    dependency_project = Project.get(slug, auth)
    required_version = dependency_project.get_specific_version(semantic_version)

    download_version(required_version, f"{dir}/..")

def download_version(version: Project.Version, dir):
  files = version.files

  dependencies = version.dependencies

  for dependency in dependencies:
     files.extend(dependency.version.files)

  # skips = 0
  downloaded_files = len(files)

  for file in files:
    skipped = download_file(file, dir)
    # skips += skipped
    downloaded_files -= skipped
  
  return downloaded_files


def to_tags_json(namespace, type):
    return f'''{{
    "values": [
        "{namespace}:{type}"
    ]
}}'''


def to_mcmeta_json(description):
    return f'''{{
	"pack": {{
		"pack_format": 13,
		"description": "{description}"
	}}
}}'''


def to_project_json(name, namespace, description):
    return f'''{{
    "name": "{name}",
    "namespace": "{namespace}",
    "version": "1.0.0",
    "description": "{description}",
    "release_type": "release",
    "game_versions": [
        
    ],projects
    "categories": [
        
    ],
    "dependencies": {{
        
    }}
}}'''


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
    from util import json_to_dependencies

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

def main():
  args = parse_args(sys.argv[1:])

  if args["flags"].count("help") != 0:
    dpm_help(args)
    return
    

  match args["action"]:
    case "init":
      init(args["dir"])

    case "publish":
      if args["auth"]:
        publish_project(args["dir"], args["auth"])
      else:
        print("Please specify --auth to publish a project")

    case "install":
      install(args["data"], args["dir"], args["auth"])

main()
