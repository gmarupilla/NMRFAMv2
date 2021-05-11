def parse_metadata(metafile_path):
    ret = {}
    try:
        with open(metafile_path, 'r') as f:
            for line in f:
                tokens = line.split(",")

                if line == 0:
                    key = "Parameters"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != "Parameters":
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 1:
                    key = "Standard"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 2:
                    key = "Frequency"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 3:
                    key = "Tissue"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 4:
                    key = "Species"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 5:
                    key = "pH"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 6:
                    key = "Volume"
                    if len(tokens) != 2:
                        print("Error: Not correct length in metadata file")
                    if tokens[0] != key:
                        print("Error: Not corrent key in metadata file: {key}".format(key=key))
                    ret[key] = tokens[1]
                elif line == 7:
                    if len(tokens) != 0:
                        print("Error: Not correct length in metadata file")

    except Ex:
        return None

    return ret
