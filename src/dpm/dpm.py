from help import dpm_help
from parse_args import parse_args
from install import *
from publish import *
from generators import *
# -------------------

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
