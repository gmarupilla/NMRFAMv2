"""
#### Generic "Writer"
The ResultsWriter has been written s.t. it can be easily replaced if the way in which we would
like to write results changes. For example, in the future we may want to replace the 
ResultsWriter with a writer to an SQL database or flat file system. Regardless of the "Writer"
that is used, the remaining portion of the code should be able to exist without change while
the only thing that will change will be this package. 

No matter which "Writer" is used, a "Writer" will probably have some sort of username associated
with it that will map to a client. 

A "Writer" will abstract away all writes AND reads to a DB, flat file, file system, etc..

#### This "Writer": ResultsWriter
The "ResultsWriter" handles all writes AND reads to a specific, statically defined, 
directory structure. 


"""


class ResultsWriter:
    # Initialize a Results Writer with a path
    def __init__(self, db_path):
        self.db_path = db_path

    def createNewUserDirectory(self, username):
        pass
