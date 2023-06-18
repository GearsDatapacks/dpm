def to_sentence_case(sentence):
    return sentence.title().replace('-', ' ').replace('_', ' ')

def to_slug(namespace):
    namespace = to_sentence_case(namespace)
    namespace = namespace.replace(' ', '-')
    return namespace.lower()

def remove_file_extension(file_name):
    return '.'.join(file_name.split('.')[:-1])

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

def to_tags_json(namespace, type):
    return f'''{{
    "values": [
        "{namespace}:{type}"
    ]
}}'''


def to_mcmeta_json(description):
    return f'''{{
	"pack": {{
		"pack_format": 13,
		"description": "{description}"
	}}
}}'''


def to_project_json(name, namespace, description):
    return f'''{{
    "name": "{name}",
    "namespace": "{namespace}",
    "version": "1.0.0",
    "description": "{description}",
    "release_type": "release",
    "game_versions": [
        
    ],projects
    "categories": [
        
    ],
    "dependencies": {{
        
    }}
}}'''
