from typing import Optional

from time import time

import os

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import requests

import gzip
import io

import json


THIS_DIR = os.path.dirname(__file__)
TOKEN_FILE = os.path.join(THIS_DIR, "token.json")


CHROMEDRIVER_PATH = "G:/NachoBot/chromedriver_downloader/chromedriver-win64/chromedriver.exe"
SLEEP_TIME = 3

EXPIRES_KEY = "accessTokenExpirationTimestampMs"
TOKEN_KEY = "accessToken"

TOKEN_URL_ID = "api/token"

BASE_SPOTIFY_URL = "https://open.spotify.com/"