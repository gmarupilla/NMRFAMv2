import json
from typing import Optional


class User:
    # After any change is made to config_info, we will save the config info
    def __init__(self, directory):
        self.directory = directory
        self.config_info = self.load_config_info()

    def load_config_info(self):
        try:
            with open(self.directory + '/config.txt') as json_file:
                return json.load(json_file)

        except Exception as e:
            print("Failed to load the config file")
        return None


def write_user(self):
    with open(self.directory + '/config.txt', 'w') as outfile:
        # TODO: determine `data`
        # json.dump(data, outfile)
        pass


class UserHandler:
    def __init__(self):
        self.db = UserDatabase()

    def create_new_user(self, username) -> bool:
        # If user already exists
        if self.db.lookup_user_directory(username) is not None:
            return False
        else:
            pass

    # Create user

    def get_user(self, username) -> Optional[User]:
        directory = self.db.lookup_user_directory(username)
        # If user does not exist
        if directory is None:
            return None
        # If user exists
        else:
            return User(directory)


class UserDatabase:
    # Need an encrypted code to make access secure
    def __init__(self):
        self.userToDirectoryDict = {
            "hamid34": "/aow403iw",
            "ehsan22": "/xlzjeiwi",
            "nan345": "/oxje8200",
            "grant52": "/os0ij320"
        }

    def lookup_user_directory(self, username) -> Optional[str]:
        if username in self.userToDirectoryDict:
            return self.userToDirectoryDict[username]
        else:
            return None
