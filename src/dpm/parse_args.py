def parse_args(args: list[str]):
  result = {
    "action": None,
    "data": None,
    "auth": None
  }

  pos = 0

  while pos < len(args):
    arg = args[pos]

    arg = aliases(arg)

    match arg:
      case "init":
        result["action"] = "init"
      
      case "install":
        result["action"] = "install"
        installs = parse_install(args, pos)
        result["data"] = installs["data"]
        pos = installs["pos"]
      
      case "publish":
        result["action"] = "publish"
      
      case _:
        if arg.startswith("--"):
          pos += 1
          arg_name = arg[2:]
          result[arg_name] = args[pos]
        
        else:
          raise Exception(f'Unexpected argument "{arg}"')

    pos += 1

  
  return result

def parse_install(args: list[str], pos: int):
  installs = []

  for i in range(pos + 1, len(args)):
    arg = args[i]

    if arg.startswith("--"):
      break
    
    installs.append(arg)
  
  return {
    "data": installs,
    "pos": i - 1
  }

def aliases(arg):
  match arg:
    case "i":
      return "install"
    case _:
      return arg
