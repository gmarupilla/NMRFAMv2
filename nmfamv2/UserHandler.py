import os

import json


class User:
    # After any change is made to config_info, we will save the config info
    def __init__(self, directory):
        self.directory = directory
        self.config_info = self.loadConfigInfo()

    def loadConfigInfo(self):
        try:
            with open(self.directory + '/config.txt') as json_file:
                return json.load(json_file)

        except Ex:
            print("Failed to load the config file")
        return None


def writeUser(self):
    with open(self.directory + '/config.txt', 'w') as outfile:
        json.dump(data, outfile)


class UserHandler:
    def __init__(self):
        self.db = UserDatabase()

    def createNewUser(self, username) -> bool:
        # If user already exists
        if self.db.lookupUserDirectory(username) is not None:
            return False
        else:
            pass

    # Create user

    def getUser(self, username) -> Optional[User]:
        directory = self.db.lookupUserDirectory(username)
        # If user does not exist
        if directory is None:
            return None
        # If user exists
        else:
            return User(directory)


class UserDatabase():

    # Need an encrypted code to make access secure
    def __init__(self):
        self.userToDirectoryDict = {
            "hamid34": "/aow403iw",
            "ehsan22": "/xlzjeiwi",
            "nan345": "/oxje8200",
            "grant52": "/os0ij320"
        }

    def lookupUserDirectory(self, username) -> str:
        if username in self.userToDirectoryDict:
            return self.userToDirectoryDict[username]
        else:
            return None
