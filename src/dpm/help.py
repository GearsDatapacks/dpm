def dpm_help(args):
  action = args["action"]

  if not action:
     print(
"""usage: dpm <action> [options]
Actions:
init                            Initialise a DPM project
install <datapacks>             Add datapacks as dependencies
install                         Download all dependencies
publish                         Publish your DPM project to Modrinth (requires --auth)

Options:
--auth <auth>      Specify a Modrinth authorisation token
--help             Show information on a specific DPM command""")

  if action == "init":
    print(
"""Initialise a DPM project

Usage:
dpm init

Creates a project.json file with information about your datapack""")

  elif action == "install":
     print(
"""Add specified datapacks as dependencies

Usage:
dpm install code-of-copper item-utils
dpm install

If left blank, it will download all dependencies of te current project

aliases: i""")

  elif action == "publish":
    print(
"""Publish your DPM project to Modrinth (requires --auth)

Usage:
dpm publish --auth foo

Zips up your datapack files and uses the infromation in the project.json file to create a version for the datapack on Modrinth""")

  else:
    raise Exception(f'Unexpected action "{action}"')
