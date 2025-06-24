import os

import json


#TODO: Add To Consider Exception
def read_json(file: str,
              default={}):
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
    if not os.path.isfile(file):
        return data

    try:
        f = open(file, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
    except:
        return default

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
    json_string = json.dumps(data, indent=4)

    f = open(file, "w")
    f.write(json_string)
    f.close()

