import json


def remove_null_values(json):
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})

    return result


def to_image_from_json(json):
    ...


def json_to_query_params(json_):
    result = ''
    for key, value in json_.items():
        result += f'{key}={json.dumps(value)}&'
    return result
