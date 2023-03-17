# Pyrinth
This is a python library that interacts with the Modrinth API


When you are using the source code and NOT the package, put your main file in the `src` directory

### Basic Example

```py
modrinth_user = User(
    'modrinth_username', 'authorization_token'
)
# This function needs an authorization token
print("Your followed projects:")
followed_projects = modrinth_user.get_followed_projects()
for project in followed_projects:
    print(project)
```
