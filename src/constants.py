import os

BASE_API_URL = "https://amp-api.music.apple.com/v1/catalog/"
BASE_SIMPLER_API_URL = "https://api.music.apple.com/v1/catalog/"
BASE_APPLE_URL = "https://music.apple.com/"


API_URL = f"{BASE_API_URL}us/"
SIMPLER_API_URL = f"{BASE_SIMPLER_API_URL}us/"
APPLE_URL = f"{BASE_APPLE_URL}us/"


SRC_FOLDER = os.path.dirname(__file__)
PROJECT_FOLDER = os.path.dirname(SRC_FOLDER)
DATA_FOLDER = os.path.join(PROJECT_FOLDER, "data")