<div align="center">
  <a href="https://github.com/GearsDatapacks/dpm">
    <img src="logo.png" alt="Logo" height="80">
  </a>

<h1 align="center">DPM</h1>
  <p align="center">
    <strong>DPM (Datapack package manager) is a package manager for Minecraft datapacks, based on npm for node.js.</strong>
  </p>
</div>

## Usage
**To use DPM, first you have to [install it](#installation).**

DPM has a variety of subcommands.

### Init
Some DPM functions require an initialised project. To initialise a DPM project, open the terminal in your datapack folder (the one containing pack.mcmeta), and run `dpm init`. This will ask some questions and then generate a file named `project.json`. 
It will also create a file named `dpmconfig.json`, which changes some of the functionality of the dppm command. More information [here](#config)

### Install
Install downloads datapacks into your world or as dependencies of another datapack.

To install a datapck into your world, open the terminal in your `<world_save>/datapacks` folder.  
Then, simply type `dpm install ` followed by the datapack id or slug on modrinth. (This will usually be an alphanumeric version of the title, e.g. `code-of-copper`).  
If everything goes correctly, it will download the datapack file alongside any dependencies that it might have.  
Then, load up your world and enjoy!

**If you are in a dpm project,**  
DPM will add the installed datapack as a dependency.

By default, DPM will install the latest stable release of specified datapacks. You can override this behaviour with the following:  
`dpm install code-of-copper@0.1.0` - installs the version "0.1.0" of Code of Copper  
`dpm install code-of-copper@latest` - installs the very latest version of Code of Copper

If you simply run `dpm install` with no arguments, it will download all dependencies that are stored in your project JSON.

### Publish
DPM allows you to publish a datapack without manually uploading it to Modrinth. If you run `dpm publish`, it will extract the settings from your project json, zip up your files and upload it directly to Modrinth.  
**Note: You must give you Modrinth auth token using the --auth flag, otherwise dpm doesn't have permission to upload the pack.**

### Alias
The alias command allows you to create aliases for auth tokens.  
This allows you to use your authorisation without having to copy-paste it every time.  
Run `dpm alias <alias-name> <auth>`, and whenever you use that alias name in `--auth`, it will replace it with the auth you give it.

### Create
Using `dpm create <template-name> <project-name>`, you can generate a datapack from a selection of templates.  
Run `dpm create --help` for a list of them.

**You can see more information by running `dpm [command] --help`**

## Config
At the moment, there are only 2 config options to be found in the `dpmconfig.json` file.

`include_files` - Additional files to include in the datapack when publishing. This supports file match syntax, e.g. `foo.*`  
`exclude_files` - Files to exclude from the datapack when publishing, overriding the default included files. This supports file match syntax, e.g. `*.json`  

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
