class Group:
    def __init__(self):
        pass


class Metadata:

    # To initialize a spectrum, at the bare minimum, one must have a ppm list and a values list
    def __init__(self, parsed_data):
        self.valid = False
        self.standard = None
        self.frequency = None
        self.tissue = None
        self.species = None
        self.pH = None
        self.volume = None
        self.groups = []
        self.parsed_data = parsed_data

    def fill(self):
        error_dict = {
            "InvalidArgsCount": "Line does not have enough args",
            "InvalidFirstParam": "First Param does not have the correct key, should be ",
            "ValueIsNotNumber": "Value is not a number",
        }
        self.valid = True

        # Line 0
        line = 0
        key = "Parameters"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return
        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        # Line 1
        line = 1
        key = "Standard"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            return

        self.standard = self.parsed_data[line][1]

        # Line 2
        line = 2
        key = "Frequency"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if not self.parsed_data[line][1].isnumeric():
            error = error_dict["ValueIsNotNumber"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        self.standard = int(self.parsed_data[line][1])

        # Line 3
        line = 3
        key = "Tissue"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        self.species = self.parsed_data[line][1]

        # Line 4
        line = 4
        key = "pH"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        self.pH = float(self.parsed_data[line][1])

        # Line 5
        line = 5
        key = "Volume"
        if len(self.parsed_data[line]) != 2:
            error = error_dict["InvalidArgsCount"]
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        if self.parsed_data[line][0] != key:
            error = error_dict["InvalidFirstParam"] + key
            print("[Metadatareader] line {linenumber}: {error}".format(linenumber=line, error=error))
            self.valid = False
            return

        self.volume = float(self.parsed_data[line][1])

    def isComplete(self):
        pass
