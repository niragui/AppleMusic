import requests

import traceback

from time import sleep

from .exceptions import ConnectionError, InvalidToken
from ..common.exceptions import InvalidID

EMPTY_CODE = 40403
CODE_FIELD = "code"

BASIC_HEADER = {}
BASIC_HEADER["authority"] = "amp-api.music.apple.com"
BASIC_HEADER["method"] = "GET"
BASIC_HEADER["scheme"] = "https"
BASIC_HEADER["Accept"] = "*/*"
BASIC_HEADER["Origin"] = "https://music.apple.com"

APPLE_BASIC_LINK = "https://music.apple.com/us/browse/top-charts/"
APPLE_TOKEN_LINK = "https://music.apple.com/assets/index-82896190.js"

TOKEN_ID = "const Su=\""

MAX_ATTEMPTS = 5

INVALID_ID_REASON = "Resource with requested id was not found"


class AppleSession():
    def __init__(self) -> None:
        self.session = None
        self.token = None
        self.header = None
        self.start_session()

    def log(self,
            msg: str):
        """
        Log the given message in the corresponding place
        depending on what was previously set.

        Parameters:
            - msg: String to log
        """
        #TODO: Add Logging Instance
        print(msg)

    def start_session(self):
        """
        Sets the session to save the token and headers needed.
        """
        self.session = requests.session()

        response = self.session.get(APPLE_BASIC_LINK)
        if response.status_code // 100 != 2:
            raise ConnectionError(f"Could Not Connect To The Base Website [{response.reason}]")

        token_response = self.session.get(APPLE_TOKEN_LINK)
        if token_response.status_code // 100 != 2:
            raise ConnectionError(f"Could Not Connect To Read The Token [{token_response.reason}]")

        token_data = token_response.content.decode("utf-8")

        self.token = None
        self.set_token(token_data)

        if not isinstance(self.token, str):
            raise InvalidToken(f"Token Read Has Not A Valid Type [{type(self.token)}]")

        self.header = BASIC_HEADER.copy()
        self.header["Authorization"] = "Bearer " + self.token

        self.session.headers.update(self.header)

    def set_token(self,
                  token_content: str):
        """
        Reads the token from the content given by the API endpoint
        and sets it in the class attribute

        Parameters:
            - token_content: Content returned by the API endpoint
        """
        self.token = None

        for line in token_content.split("\n"):
            start = line.find(TOKEN_ID)
            if start >= 0:
                start += len(TOKEN_ID)
                end = line.find("\"", start)
                self.token = line[start: end]

        if self.token is None:
            raise InvalidToken(f"Could Not Find Token ID In Content")

    def check_session(self,
                      max_attempts: int = MAX_ATTEMPTS):
        """
        Check if the session is set, if not it tries to reset it
        """
        if self.session is not None:
            return

        attempts = 0
        while True:
            try:
                self.start_session()
                break
            except Exception as err:
                self.log(traceback.format_exc())
                attempts += 1
                if attempts >= max_attempts:
                    self.log(f"Stop Trying To Connect After {attempts} Attempts")
                    raise err
                else:
                    sleep(5)

    def get(self,
            link: str,
            max_attempts: int = MAX_ATTEMPTS):
        """
        Use the session to request for a given link.

        Parameters:
            - link: URL to request
            - max_attempts: Amount of times to retry the query
        """
        self.check_session()

        attempts = 0

        while True:
            try:
                response = self.session.get(link)

                if response.status_code // 100 != 2:
                    try:
                        errors = response.json()["errors"]
                        if int(errors[0][CODE_FIELD]) == EMPTY_CODE:
                            return None
                        message = ", ".join(error["detail"] for error in errors)
                    except:
                        message = ""

                    if message == INVALID_ID_REASON:
                        raise InvalidID(f"Invalid ID Request")

                    raise ConnectionError(f"Could Not Read Data [{response.reason} | {message}]")

                return response
            except InvalidID as err:
                raise err
            except Exception as err:
                attempts += 1
                if attempts >= max_attempts:
                    self.log(f"Stop Trying To Get {link} After {attempts} Attempts")
                    raise err

                self.log(traceback.format_exc())
                sleep(5)