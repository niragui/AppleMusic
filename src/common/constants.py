import os

from ..constants import DATA_FOLDER
from .json_handle import read_json

COUNTRIES_FILE = os.path.join(DATA_FOLDER, "countries.json")
COUNTRIES = read_json(COUNTRIES_FILE, {})