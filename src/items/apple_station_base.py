from typing import Optional

from urllib.parse import urlencode

from ..session.applesession import AppleSession
from .apple_item import AppleItem, AppleTypes

from .artwork import ArtWork

BASE_ASSETS_URL = "https://amp-api.music.apple.com/v1/play/assets"


class PlayParams():
    def __init__(self,
                 params: dict) -> None:
        self.play_id = params["id"]
        self.kind = params["kind"]
        self.format = params["format"]
        self.station_hash = params["stationHash"]
        self.has_drm = params["hasDrm"]
        self.media_type = params["mediaType"]

        self.params = params

    def get_assets_url(self):
        """
        Returns the assets url for the given params
        """
        params_encoded = urlencode(self.params)

        url = f"{BASE_ASSETS_URL}?{params_encoded}"

        return url


class AppleStationBase(AppleItem):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = False,
                 read_extra: bool = False):
        self._name = ""

        self._live = False

        self._artwork = None
        self._play_params = None

        self._media_kind = None
        self._supported_drms = []

        self._tag = ""
        self._description = ""

        super().__init__(item_id, AppleTypes.STATION, session, read_data, read_extra)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        attributes = data["attributes"]

        self._name = attributes["name"]

        edit_notes = attributes.get("editorialNotes", {})
        self._tag = edit_notes.get("tagline", "")
        self._description = edit_notes.get("short", "")

        self._supported_drms = attributes.get("supportedDrms", [])

        self._media_kind = attributes.get("mediaKind", None)
        self._live = attributes.get("isLive", False)

        self._artwork = ArtWork(attributes.get("artwork"))
        self._play_params = PlayParams(attributes.get("playParams"))

    def get_image(self,
                  width: Optional[int] = None,
                  height: Optional[int] = None):
        """
        Returns the url of the image for the artwork

        Parameters:
            - width: Width to use. If None, the max possible will be used
            - height: Height to use. If None, the max possible will be used
        """
        return self._artwork.get_image(width, height)

    @property
    def image(self):
        """
        Returns the url of the image for the artwork in max quality
        """
        return self.get_image()

    def get_name(self, reset_values: bool = False):
        """
        Get the name of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_name", reset_values)

    @property
    def name(self):
        """
        Get the name of the playlist.
        """
        return self._name

    def get_description(self, reset_values: bool = False):
        """
        Get the description of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_description", reset_values)

    @property
    def description(self):
        """
        Get the description of the playlist.
        """
        return self._description

    def get_play_params(self):
        """
        Request the API for the Play Params
        """
        if self._play_params is None:
            raise AttributeError("Unset Item")

        play_url = self._play_params.get_assets_url()

        response = self.session.get(play_url)

        if response is None:
            raise ConnectionError(f"Invalid Id For Request")

        return response.json()

    def __repr__(self) -> str:
        return f"Apple Station (Name: {self._name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Station (Name: {self._name} | ID: {self.item_id})"