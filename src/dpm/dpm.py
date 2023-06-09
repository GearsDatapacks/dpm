from argparse import ArgumentParser
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
from pyrinth import *
# -------------------


def download_file(file, dir, longest_file_name):

    # Create the full file path by joining the folder path and file name
    path = f"{dir}/{file.filename}"

    # If the download was skipped
    if os.path.exists(path):
        print(
            f"{file.filename.ljust(longest_file_name, ' ')} already downloaded... skipping"
        )
        return [0.0, 1]

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
            filename = file.filename.ljust(longest_file_name, ' ')
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

    return [float(time_taken), 0]

def install(projects, dir, auth):
    download_dir = dir

    if os.path.exists(f'{dir}/project.json'):
        download_dir = f'{dir}/..'

    for project in projects:
        download_project(project, download_dir, auth)
        if os.path.exists(f'{dir}/project.json'):
          add_dependency(project, dir, auth)
          
def add_dependency(dependency, dir, auth):
  with open(f"{dir}/project.json", "r") as f:
    project = json.loads(f.read())
  
  
  dependency_project = Modrinth.get_project(dependency, auth)
  latest_version = dependency_project.get_latest_version().version_model.version_number

  if not project["dependencies"]:
      project["dependencies"] = {}

  print(dependency)

  project["dependencies"][dependency] = latest_version

  print(project)
  with open(f"{dir}/project.json", "w") as f:
      f.write(json.dumps(project, indent=2))

def download_project(project_id, dir, auth=''):
    
    project = Modrinth.get_project(project_id, auth)
    
    # If no project is found, print an error message and return None
    if not project:
        return None
    
    print(f"Project '{to_sentence_case(project.get_slug())}' found")

    # Get the latest version of the project and its files
    latest = project.get_latest_version(loaders=["datapack"])

    if not latest:
        return None
    
    project_files = latest.get_files()
    
    # Get the dependencies of the project
    dependencies = project.get_dependencies()
    
    # Initialize an empty list to keep track of all files that need to be downloaded
    downloading_files = []

    # Add the project files to the downloading_files list
    downloading_files.extend(project_files)

    # If there are any dependencies, add their latest versions' files to the downloading_files list
    if dependencies:
        for dependency in dependencies:
            downloading_files.extend(
                dependency.get_latest_version().get_files()
            )

    # Calculate the length of the longest filename among all files that need to be downloaded ( for padding )
    longest_file_name = -1
    for file in downloading_files:
        if len(file.filename) > longest_file_name:
            longest_file_name = len(file.filename)

    # Keep track of how much time has taken to download all files
    # Keep track of how many files are skipped
    total_time_taken = 0
    skips = 0
    downloaded_files = len(downloading_files)

    for file in downloading_files:
        result = download_file(file, dir, longest_file_name)
        total_time_taken += result[0]
        skips += result[1]
        downloaded_files -= result[1]

    if skips != len(downloading_files):
        print(f"{downloaded_files} file(s) downloaded in {total_time_taken:.2f}s")
    else:
        print("Download no extra files")
    option = input("Would you like to open the projects modrinth page (y/N)? ").lower()
    if option == "y" or option == "yes":
        webbrowser.open(
            f"https://modrinth.com/datapack/{project.project_model.id}"
        )


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
        
    ],
    "categories": [
        
    ],
    "dependencies": {{
        
    }}
}}'''


def create_project(namespace):
    namespace = to_namespace(namespace)
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


def search_project(query):
    projects = Modrinth.search_projects(
        query, facets=[["categories:datapack"]])
    for i, project in enumerate(projects):
        index = str(i+1).ljust(2, ' ')
        print(f'{index} | ' + project.search_result_model.title)
    print("If your project is not in this list, please try being more specific with your search query")
    option = input("Select a project: ")
    if option == '':
        return
    option = int(option)
    if option > len(projects) or option <= 0:
        print("Invalid project number.")
        return
    project = Modrinth.get_project(
        projects[option-1].search_result_model.project_id)
    print(f"Selected project: {project.project_model.title}")
    download_project(project.project_model.id)

def format_dependencies(dependencies):
    result = []

    dependency_array = list(dependencies.items())

    for dependency in dependency_array:
        slug = dependency[0]
        version_number = dependency[1]

        dependency_project = Modrinth.get_project(slug)
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

    modrinth_project: Project = Modrinth.get_project(slug, auth)

    get_user = User.from_auth(auth)
    user = User(
        get_user.username, auth
    )


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

    project = Modrinth.get_project(slug, auth)

    if not project:
        print(f"Project '{title}' with slug '{slug}' was not found")
        return
    
    version = project.create_version(auth, VersionModel(
        name=version_title, version_number=version_number, dependencies=dependencies,
        game_versions=game_versions, release_type=version_type, loaders=['datapack'],
        featured=True, files=[zip_path]
    ))

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


if __name__ == "__main__":
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--install', metavar="Project ID", help="Install a project", action='append', nargs='+')
    group.add_argument('--publish', metavar="Datapack Folder Name", help="Publish your datapack to Modrinth")
    group.add_argument('--init', help="Initialise a DPM project", default="")
    parser.add_argument('-a', '--auth', metavar="Authorization Token", help="Specify an authorizaton token to use", default='')
    parser.add_argument('--dir', metavar="Target Directory", help="Specify the target directory", default='')

    args = parser.parse_args()

    if args.install:
        install(args.install[0], args.dir, args.auth)
    if args.publish:
        if args.auth:
            publish_project(args.dir, args.auth)
        else:
            print("Please specify --auth to publish a project")
    if args.init:
        init(args.dir)
