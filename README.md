# DPM

**DPM (Datapack package manager) is a package manager for Minecraft datapacks, based on npm for node.js.**

## Usage
**To use DPM, first you have to [install it](#installation).**

DPM can be used in two ways.

### 1. Installing datapacks in your world
To install a datapck into your world, open the terminal in your `<world_save>/datapacks` folder.  
Then, simply type `dpm install ` followed by the datapack id or slug on modrinth. (This will usually be an alphanumeric version of the title).  
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

## Installation

**To use DPM, you must first install python.**

### Linux
1. Download the latest version (or any version you desire) from the releases page.

2. Unzip the file you downloaded. You should get a folder containing `install.sh`, `dpm.sh` and the `src` folder.

3. Run `install.sh`. You will need to enter your password to install it correctly. (You will also probably have to give it executable permissions)

### Mac
Try following the [linux instructions](#linux). Untested as of yet.

### Windows
Windows support coming soon

## How DPM Works

DPM uses [Pyrinth](https://github.com/RevolvingMadness/Pyrinth), a python interface with the Modrinth API. It uses pyrinth to download, publish and edit projects. Thank you to RevolvingMadness for making that!

## Credits
Thank you to RevolvingMadness for creating Pyrinth, the backbone of this tool.
RevolvingMadness also helped with the early versions of DPM, so thank you for that.
