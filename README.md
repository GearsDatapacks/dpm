# DPM

**DPM (Datapack package manager) is a package manager for Minecraft datapacks, based on npm for node.js.**

## Usage
**To use DPM, first you have to [install it](#installation).**

DPM can be used in two ways.

### 1. Installing datapacks in your world
To install a datapck into your world, open the terminal in your `<world_save>/datapacks` folder.  
Then, simply type `dpm install ` followed by the datapack id or slug on modrinth. (This will usually be an alphanumeric version of the title, e.g. `code-of-copper`).  
If everything goes correctly, it will download the datapack file alongside any dependencies that it might have.  
Then, load up your world and enjoy!

### 2. Managing dependencies in your datapack
DPM also lets you to manage dependencies within your own datapacks. To initialise a DPM project, open the terminal in your datapack folder (the one containing pack.mcmeta), and run `dpm init`. This will ask some questions and then generate a file named `project.json`. 

**Installing dependencies**  
Installing dependencies is as simple as running `dpm install <datapack id/slug>`. This will add an entry to your `project.json`.

If you simply run `dpm install` with no arguments, it will download all dependencies that are stored in your project JSON.

**Publishing**  
DPM allows you to publish a datapack without manually uploading it to Modrinth. If you run `dpm publish`, it will extract the settings from your project json, zip up your files and upload it directly to Modrinth.  
**Note: You must give you Modrinth auth token using the --auth flag, otherwise dpm doesn't have permission to upload the pack.**

**You can see more information by running `dpm [command] --help`**  
  
## Installation

1. Download the corresponding binary for your operating system from the releases page
2. Open a terminal and run the dpm binary
3. I would suggest exporting the path to the binary, so you can use `dpm` anywhere

## How DPM Works

DPM uses [Gorinth](https://github.com/GearsDatapacks/Gorinth), an interface with the Modrinth API. It uses gorinth to download, publish and edit projects.

## Contributing

DPM is written in golang, so to develop it you must have go installed on your machine.  
To make changes to dpm, simply clone the repository, modify the source code, then open a terminal in the folder and run `go build`. This generates a new dpm binary file.

## Why I switched to Golang
If you saw the other branch, or looked at early versions of dpm, you will know that it was originally written in python.  
There were a few reasons that I originally wrote it in python:
- Python is a language which a lot of people have installed on their machine
- I was already familiar with it
- Pyrinth meant I didn't have to deal with the Modrinth API

But I decided to make the switch because:
- Golang is compiled, meaning people don't need anything preinstalled to use it
- I was having trouble with python and pip
- Pyrinth wasn't working properly, so I thought I should just write my own version
