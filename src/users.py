from urllib import response
import requests as r
import json
from src.projects import Project


class Notification:
    def __init__(self, notification):
        self.id = notification['id']
        self.user_id = notification['user_id']
        self.type = notification['type']
        self.title = notification['title']
        self.text = notification['text']
        self.link = notification['link']
        self.read = notification['read']
        self.created = notification['created']
        self.actions = notification['actions']
        self.project_title = self.title.split('**')[1]


class TeamMember:
    def __init__(self, team_member):
        self.team_id = team_member['team_id']
        self.user = User(team_member['user']['username'], ignore_warning=True)
        self.role = team_member['role']
        self.permissions = team_member['permissions']
        self.accepted = team_member['accepted']
        self.payouts_split = team_member['payouts_split']
        self.ordering = team_member['ordering']


class User:
    def __init__(self, username, authorization='', ignore_warning=False) -> None:
        self.auth = authorization
        if self.auth != '':
            self.raw_response = r.get(
                f'https://api.modrinth.com/v2/user',
                headers={
                    'authorization': self.auth
                }
            )
            if not self.raw_response.ok:
                raise Exception("Invalid auth token")

        if self.auth == '':
            self.raw_response = r.get(
                f'https://api.modrinth.com/v2/user/{username}'
            )
            if not ignore_warning:
                print('[WARNING] Some functions won\'t work without an auth key')

        self.response = json.loads(self.raw_response.content)
        self.username = self.response['username']
        self.id = self.response['id']
        self.github_id = self.response['github_id']
        self.name = self.response['name']
        self.email = self.response['email']
        self.avatar_url = self.response['avatar_url']
        self.bio = self.response['bio']
        self.created = self.response['created']
        self.role = self.response['role']
        self.badges = self.response['badges']
        self.payout_data = self.response['payout_data']

    def get_followed_projects(self) -> list[Project]:
        """This function gets a users followed projects

        Returns:
            list[Project]: The list of projects that the user follows
        """
        if self.auth == '':
            raise Exception("get_followed_projects needs an auth token.")
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{self.username}/follows',
            headers={
                'authorization': self.auth
            }
        )

        followed_projects = []
        projects = json.loads(raw_response.content)
        for project in projects:
            followed_projects.append(Project(project))

        return followed_projects

    def get_notifications(self) -> list[Notification]:
        """This function gets a users notifications

        Returns:
            list[Notification]: The list of notifications that was found on the user
        """
        if self.auth == '':
            raise Exception("get_notifications needs an auth token.")
        raw_response = r.get(
            f'https://api.modrinth.com/v2/user/{self.username}/notifications',
            headers={
                'authorization': self.auth
            }
        )
        response = json.loads(raw_response.content)

        return [Notification(notification) for notification in response]

    def get_project(self, id):
        """This function finds a project by ID, then returns it

        Args:
            id (str): The ID of the project

        Returns:
            Project: The project that was searched using the id
        """
        if self.auth == '':
            raise Exception("get_project needs an auth token.")
        raw_response = r.get(
            f'https://api.modrinth.com/v2/project/{id}',
            headers={
                'authorization': self.auth
            }
        )
        response = json.loads(raw_response.content)
        return Project(response)

    def get_projects(self, ids) -> list[Project]:
        """This function finds multiple projects by IDs, then returns them

        Args:
            ids (list[str]): the IDs of the projects

        Returns:
            list[Project]: The projects that were searched using ids
        """
        if self.auth == '':
            raise Exception("get_projects needs an auth token.")
        raw_response = r.get(
            f'https://api.modrinth.com/v2/projects',
            headers={
                'authorization': self.auth
            },
            params={
                'ids': json.dumps(ids)
            }
        )
        response = json.loads(raw_response.content)
        return [Project(project) for project in response]


def get_user_from_auth(auth) -> User:
    """This function finds a user with the specified auth token

    Args:
        auth (str): The auth token to use for searching

    Returns:
        User: The user that was found using the auth token
    """
    raw_response = r.get(
        f'https://api.modrinth.com/v2/user',
        headers={
            'authorization': auth
        }
    )
    response = json.loads(raw_response.content)
    return User(response['username'], auth)


def get_users_from_auths(auths) -> list[User]:
    """This function finds multiple users with multiple specified auth token

    Args:
        auths (list[str]): The auth tokens to use for searching

    Returns:
        list[User]: The users that were found using the auth tokens
    """
    return [get_user_from_auth(auth) for auth in auths]


def get_users_from_ids(ids) -> list[User]:
    """This function finds users with the specified ids

    Args:
        ids (list[str]): The IDs of the users

    Returns:
        list[User]: The users that were searched using the IDs
    """
    raw_response = r.get(
        'https://api.modrinth.com/v2/users',
        params={
            'ids': json.dumps(ids)
        }
    )
    response = json.loads(raw_response.content)
    return [User(user['username']) for user in response]


def get_user_from_id(id) -> User:
    """This function gets a user from their id

    Args:
        id (str): The ID of the user

    Returns:
        User: The user that was found
    """
    response = r.get(
        f'https://api.modrinth.com/v2/user/{id}'
    ).json()
    return User(response['username'])


def get_team_members_of_project(id) -> list[TeamMember]:
    raw_response = r.get(
        f'https://api.modrinth.com/v2/project/{id}/members'
    )
    response = json.loads(raw_response.content)
    return [TeamMember(user) for user in response]
