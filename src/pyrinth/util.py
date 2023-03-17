import json


def remove_null_values(json: dict):
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})

    return result


def to_image_from_json(json: dict):
    from pyrinth.projects import Project
    return [Project.GalleryImage.from_json(image) for image in json]


def json_to_query_params(json_: dict):
    result = ''
    for key, value in json_.items():
        result += f'{key}={json.dumps(value)}&'
    return result
