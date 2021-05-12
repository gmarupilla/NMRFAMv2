import zipfile
import pandas as pd

"""
Lay of the land:


"""


class UserHandler(object):
    # This Object is used to access the directory that saves the results
    def __init__(self, user_directory_path, pathToMixture):
        self.user_directory_path = user_directory_path
        self.username = None
        self.pathToMixture = pathToMixture

    def addZip(self, zipfile_path):
        if self.username is None:
            print("[userHandler.py][addZip] Error")

        else:
            if zipfile.is_zipfile(zipfile_path):
                with zipfile.ZipFile(zipfile_path, 'r') as zipObj:
                    topDirName = zipObj.infolist()[0].filename
                    var = self.pathToMixture
