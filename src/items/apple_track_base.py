from typing import Optional

import datetime

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from ..session.applesession import AppleSession


class AppleTrackBase(AppleItem):
    def __init__(self,
                 track_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = False) -> None:
        self._name = ""
        self._credits = ""

        self._composers_name = ""
        self._genres_names = []

        self._album_name = ""
        self._album_id = ""
        self._album_position = 0
        self._album_disc = 0

        self._duration = 0
        self._release = None

        self._artwork = None
        super().__init__(track_id, AppleTypes.TRACK, session, read_data)

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
        self._credits = attributes["artistName"]
        self._composers = attributes.get("composerName", "")

        self._album_name = attributes["albumName"]
        self._album_position = attributes["trackNumber"]
        self._album_disc = attributes["discNumber"]

        artwork = attributes["artwork"]
        self._artwork = ArtWork(artwork)

        self._genres = attributes["genreNames"]
        self._duration = attributes.get("durationInMillis", 0)

        release_str = attributes.get("releaseDate", None)
        if release_str:
            self._release = datetime.date.fromisoformat(release_str)
        else:
            self._release = None

        url = attributes["url"]
        album_id_start = url.rfind("/") + 1
        album_id_end = url.find("?", album_id_start)

        self._album_id = url[album_id_start: album_id_end]

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
        Get the name of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_name", reset_values)

    @property
    def name(self):
        """
        Get the name of the song.
        """
        return self._name

    def get_credits(self, reset_values: bool = False):
        """
        Get the name of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_credits", reset_values)

    @property
    def credits(self):
        """
        Get the name of the song.
        """
        return self._credits

    def get_duration(self, reset_values: bool = False):
        """
        Get the duration of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_duration", reset_values)

    @property
    def duration(self):
        """
        Get the total amount of time of a song in miliseconds.
        """
        return self.get_duration()

    def __repr__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"