import fire
import requests as r
from pyrinth import *
import os


def download_file(file, longest_file_name):
    # Send a GET request to the specified file URL and stream the response
    response = r.get(file.url, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
        print(f'Error: Failed to download {file.filename}')
        return

    # Get the total size of the file from the response headers
    total_progress = int(response.headers.get('content-length', 0))

    # Set the block size for reading data from the response
    block_size = 1024

    # Initialize a variable to keep track of how much data has been downloaded
    progress = 0

    # Open a file for writing in binary mode
    with open(file.filename, 'wb') as f:

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
                f'Downloading {filename}: [{bar}] / {percent}',
                end='\r'
            )
    print("\n", end='')


def download_project(download):
    # Get information about the specified project from Modrinth
    project = Modrinth.get_project(download)
    # If no project is found, print an error message and return None
    if not project:
        print(f"Project {download} was not found")
        return None

    # Get the latest version of the project and its files
    project_files = project.get_latest_version().get_files()
    # Get the dependencies of the project
    dependencies = project.get_dependencies()
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
                dependency.get_latest_version().get_files())

    # Calculate the length of the longest filename among all files that need to be downloaded
    longest_file_name = -1
    for file in downloading_files:
        if len(file.filename) > longest_file_name:
            longest_file_name = len(file.filename)

    # For each file in downloading_files,
    for file in downloading_files:
        # If it is not already present in the current directory,
        if file.filename not in os.listdir():
            # Download it using a separate function named download_file
            download_file(file, longest_file_name)
        else:
            # Otherwise, print a message indicating that it has already been downloaded and will be skipped
            print(
                f"{file.filename.ljust(longest_file_name, ' ')} already downloaded... skipping"
            )


# Usage python dpm.py --download project-id-or-slug
if __name__ == "__main__":
    fire.Fire(download_project)
