from argparse import ArgumentParser
import shutil
import webbrowser
import requests as r
import os
# TURN OFF YOUR FORMATTER, IT WILL PUT THIS IN THE WRONG ORDER AND IT WILL STOP WORKING!!!
import sys
# sys.path.append(f"C:/Users/{os.getlogin()}/OneDrive/Desktop/Pyrinth/src") # Testing - Windows
sys.path.append(f"path/to/pyrinth/src") # Testing - Other OS's
from pyrinth import *
# -------------------


def to_sentence_case(sentence):
    return sentence.title().replace('-', ' ').replace('_', ' ')


def remove_file_extension(file_name):
    return '.'.join(file_name.split('.')[:-1])


def download_file(file, folder_path, longest_file_name):
    # Create the full file path by joining the folder path and file name
    file_path = folder_path + '/' + file.filename

    # Check if the specified folder exists
    if not os.path.exists(folder_path):
        # If it doesn't exist, create it
        os.mkdir(folder_path)
    else:
        if os.path.exists(file_path):
            print(
                f"{file.filename.ljust(longest_file_name, ' ')} already exists... skipping")
            return

    # Send a GET request to the specified file URL and stream the response
    response = r.get(file.url, stream=True)

    # Get the total size of the file from the response headers
    total_progress = int(response.headers.get('content-length', 0))

    # Set the block size for reading data from the response
    block_size = 1024

    # Initialize a variable to keep track of how much data has been downloaded
    progress = 0

    # Open a file for writing in binary mode
    with open(file_path, 'wb') as f:

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
                f'Downloading: {filename} [{bar}] / {percent}',
                end='\r'
            )
    # Print a newline character to move to the next line
    print("\n", end='')


def download_project(project_id, auth=''):
    # Get information about the specified project from Modrinth
    project = Modrinth.get_project(project_id, auth)
    # If no project is found, print an error message and return None
    if not project:
        return None
    print(f"Project '{to_sentence_case(project.project_model.title)}' found")

    # Get the latest version of the project and its files
    latest = project.get_latest_version(loaders=["datapack"])
    if not latest:
        return None
    project_files = latest.get_files()
    main_file = project_files[0]
    # Get the dependencies of the project
    dependencies = project.get_dependencies()
    print(dependencies)
    # Initialize an empty list to keep track of all files that need to be downloaded
    downloading_files = []

    # If there are any files associated with the latest version of the project,
    # add them to the downloading_files list
    if project_files:
        downloading_files.extend(project_files)

    # If there are any dependencies, add their latest versions' files to the downloading_files list
    if dependencies:
        for dependency in dependencies:
            downloading_files.extend(
                dependency.get_latest_version().get_files()
            )

    # Calculate the length of the longest filename among all files that need to be downloaded
    longest_file_name = -1
    for file in downloading_files:
        if len(file.filename) > longest_file_name:
            longest_file_name = len(file.filename)

    for file in downloading_files:
        download_file(file, remove_file_extension(main_file.filename), longest_file_name)

    option = input("Would you like to open the projects modrinth page (y/n)? ")
    if 'y' in option:
        webbrowser.open(
            f"https://modrinth.com/datapack/{project.project_model.id}")


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
    namespace = namespace.lower()
    if ' ' in namespace:
        print("Namespace cannot contain spaces")
        return
    name = to_sentence_case(namespace)
    description = input("Enter the description of the datapack: ")
    if len(description) < 3:
        print("Warning! You will not be able to publish this datapack to modrinth if the description is under 3 characters!")
    if name == '':
        print("Name cannot be blank")
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


def publish_project(folder_name, auth):
    if not os.path.exists(folder_name):
        print(f"Could not find '{folder_name}' in the current directory")
        return

    if not os.path.exists(f"{folder_name}/project.json"):
        print(f"Could not find 'project.json' in project '{folder_name}'")
        return

    project = json.loads(open(f"{folder_name}/project.json", "r").read())
    slug = project['namespace']
    title = project['name']
    description = project['description']
    categories = project['categories']

    get_user = User.from_auth(auth)
    user = User(
        get_user.username, auth
    )
    project = user.create_project(ProjectModel(
        slug, title, description, categories,
        'optional', 'required', '',
        'LicenseRef-Unknown', 'mod'
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

    group.add_argument('-d',  '--download', metavar="Project ID", help="Download a project")
    group.add_argument('-p', '--publish', metavar="Authorization Token", help="Specify an authorizaton token to use")
    group.add_argument('-pv', '--publish-version', metavar="Authorization Token", help="Specify an authorizaton token to use")
    group.add_argument('-s',  '--search', metavar="Search Query", help="Search for a project")
    group.add_argument('-c',  '--create', metavar="Datapack Namespace", help="Create a datapack")
    parser.add_argument('-a', '--auth', metavar="Authorization Token", help="Specify an authorizaton token to use", default='')

    args = parser.parse_args()

    if args.download:
        download_project(args.download, args.auth)
    if args.search:
        search_project(args.search)
    if args.create:
        create_project(args.create)
    if args.publish:
        if args.auth:
            publish_project(args.publish, args.auth)
        else:
            print("Please specify --auth to publish a project")
    if args.publish_version:
        if args.auth:
            publish_version(args.publish_version, args.auth)
        else:
            print("Please specify --auth to publish a version")
