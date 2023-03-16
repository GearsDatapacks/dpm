import json


def remove_null_values(json: dict) -> dict:
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})

    return result


<<<<<<<< HEAD:src/pyrinth/util.py
# Returns list[Project.GalleryImage]
def to_image_from_json(json: dict) -> list[object]:
========
def to_image_from_json(json: dict):
>>>>>>>> ff4b35c (refactor: Move files into dpm folder):dpm/pyrinth/util.py
    from pyrinth.projects import Project
    return [Project.GalleryImage.from_json(image) for image in json]


def json_to_query_params(json_: dict) -> str:
    result = ''
    for key, value in json_.items():
        result += f'{key}={json.dumps(value)}&'
    return result
