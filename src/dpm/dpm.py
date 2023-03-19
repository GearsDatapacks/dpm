from argparse import ArgumentParser
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


def publish_project(dir, auth):
    if not os.path.exists(f"{dir}/project.json"):
        print(f"Could not find project.json. Please initialise a project to publish")
        return

    with open(f"{dir}/project.json", "r") as f:
        project = json.loads(f.read())

    slug = project['namespace'] or to_slug(project['name'])
    title = project['name']
    description = project['description']
    categories = project['categories']
    license = project['license']

    get_user = User.from_auth(auth)
    user = User(
        get_user.username, auth
    )

    modrinth_project: Project = Modrinth.get_project(slug, auth)

    if modrinth_project:
      modrinth_project.modify(auth=auth, title=title, description=description, categories=categories, client_side='optional', server_side='required', license_id=license)
    
    else:
      project = user.create_project(ProjectModel(
          slug, title, description, categories,
          'optional', 'required', '',
          license, 'mod'
      ))
      if project:
          print(f"Successfully published project '{title}'")
        

def publish_version(folder_name, auth):
    from util import json_to_dependencies
    if not os.path.exists(folder_name):
        print(f"Could not find '{folder_name}' in the current directory")
        return

    if not os.path.exists(f"{folder_name}/project.json"):
        print(f"Could not find 'project.json' in project '{folder_name}'")
        return

    project_json = json.loads(open(f"{folder_name}/project.json", "r").read())

    slug = project_json['namespace']
    title = project_json['name']
    version_number = project_json['version']
    dependencies = project_json['dependencies']
    game_versions = project_json['game_versions']
    version_type = project_json['release_type']

    shutil.make_archive(f"{folder_name}", 'zip', folder_name)

    project = Modrinth.get_project(slug, auth)

    if not project:
        print(f"Project '{title}' with namespace/project slug '{slug}' was not found")
        return
    
    version = project.create_version(auth, VersionModel(
        title, version_number, json_to_dependencies(dependencies),
        game_versions, version_type, ['datapack'],
        True, [f"{folder_name}.zip"]
    ))

    os.remove(f"{folder_name}.zip")

    if version:
        print(f"Successfully created version '{title}'")


if __name__ == "__main__":
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--install', metavar="Project ID", help="Install a project", action='append', nargs='+')
    group.add_argument('--publish', metavar="Datapack Folder Name", help="Create a datapack on Modrinth")
    parser.add_argument('-a', '--auth', metavar="Authorization Token", help="Specify an authorizaton token to use", default='')
    parser.add_argument('--dir', metavar="Target Directory", help="Specify the target directory", default='')

    args = parser.parse_args()

    if args.install:
        for download_args in args.install:
            for project in download_args:
                download_project(project, args.dir, args.auth)
    if args.publish:
        if args.auth:
            publish_project(args.dir, args.auth)
        else:
            print("Please specify --auth to publish a project")
