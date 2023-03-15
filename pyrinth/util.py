def remove_null_values(json):
    result = {}
    for key, value in json.items():
        if value is not None:
            result.update({key: value})

    return result
