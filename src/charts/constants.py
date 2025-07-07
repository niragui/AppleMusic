from enum import Enum

import os

from ..common.json_handle import read_json
from ..constants import DATA_FOLDER


GENRES_FILE = os.path.join(DATA_FOLDER, "genres.json")
GENRES = read_json(GENRES_FILE)


class ChartsTypes(Enum):
    ALBUMS = "albums"
    VIDEOS = "music-videos"
    PLAYLISTS = "playlists"
    TRACKS = "songs"

