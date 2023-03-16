from models import ProjectModel


empty_project = ProjectModel(
    'project_id',
    'Project Title',
    'Project Description',
    [],
    'required | required / optional / unsupported',
    'unsupported | required / optional / unsupported',
    'Project Body',
    'LicenseRef-Unkown',
    'project_type | mod / datapack',
    [],
    'issues_url',
    'source_url',
    'wiki_url',
    'discord_url',
    [
        'donation_urls'
    ],
    'license_url'
)
