from help import dpm_help
from parse_args import parse_args
import json
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
