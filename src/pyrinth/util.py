def to_sentence_case(sentence):
    return sentence.title().replace('-', ' ').replace('_', ' ')

def remove_null_values(json: dict) -> dict:
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})

    return result


# Returns list[Project.GalleryImage]
def to_image_from_json(json: dict) -> list[object]:
    from pyrinth.projects import Project
    return [Project.GalleryImage.from_json(image) for image in json]


def json_to_query_params(json_: dict) -> str:
    import json
    result = ''
    for key, value in json_.items():
        result += f'{key}={json.dumps(value)}&'
    return result

def remove_file_path(file):
    return ''.join(file.split('/')[-1])

def json_to_dependencies(json):
    from pyrinth.modrinth import Modrinth
    result = []

    for name, dep_type in json.items():
        project = Modrinth.get_project(name)
        if not project:
            print(f"Dependency '{name}' not found")
            return None
        project_id = project.get_id()
        dep = {
            "project_id": project_id,
            "dependency_type": dep_type
        }
        result.append(dep)

    return result