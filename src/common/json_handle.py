import os

import json


def read_json(file: str,
              default = {}):
    """
    Given a file, it reads it and parse
    it as a json file. If the file is not present
    it returns the default value.

    Parameters:
        - file: Path to the file to read
        - default (Optional): Default value to return in case the
            file is missing. By default it returns an empty dictionary.
    """
    data = default
    if os.path.isfile(file):
        f = open(file, "r", encoding="utf-8")
        data = json.load(f)
        f.close()

    return data


def write_json(file: str,
               data):
    """
    Given a file, and a json serializable object.
    It writes the file as a json file with the object
    information.

    Parameters:
        - file: Path to the file to save the data at.
        - data: Object to save in the json file.
    """
    f = open(file, "w")
    f.write(json.dumps(data, indent=4))
    f.close()

