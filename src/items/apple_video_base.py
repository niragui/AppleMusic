from typing import Optional

import datetime

from ..session.applesession import AppleSession
from .apple_item import AppleItem, AppleTypes

from .artwork import ArtWork


class Preview():
    def __init__(self,
                 preview_data: dict) -> None:
        self.play_url = preview_data["url"]
        self.artwork = ArtWork(preview_data["artwork"])


class AppleVideoBase(AppleItem):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = False,
                 read_extra: bool = False):
        self._name = ""
        self._credits = ""

        self._previews = []

        self._artwork = None

        self._genres = []

        self._four_k = False
        self._hdr = False

        self._duration = 0

        self._release_date = None
        super().__init__(item_id, AppleTypes.VIDEO, session, read_data, read_extra)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the music video.

        Parameters:
            - data: Data given by the Apple Music API
        """
        attributes = data["attributes"]

        self._name = attributes["name"]
        self._credits = attributes["artistName"]

        for preview in attributes["previews"]:
            self._previews.append(Preview(preview))

        self._artwork = ArtWork(attributes["artwork"])
        self._genres = attributes["genreNames"]

        self._four_k = attributes["has4K"]
        self._hdr = attributes["hasHDR"]

        self._duration = attributes["durationInMillis"]

        release_str = attributes.get("releaseDate", None)
        if release_str is None:
            self._release = None
        elif release_str.isdigit():
            self._release = datetime.date(int(release_str), 1, 1)
        else:
            self._release = datetime.date.fromisoformat(release_str)

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

    def get_release_date(self, reset_values: bool = False):
        """
        Get the release date of the album.
        Note: Sometimes the release date saved on Apple might
        not match the real release date.

        Parameters:
            - reset_values (Optional): If it should ask for the
                album information again
        """
        return self.get_attr("_release_date", reset_values)

    @property
    def release_date(self):
        """
        Get the release date of the album.
        Note: Sometimes the release date saved on Apple might
        not match the real release date.
        """
        return self._release_date

    def get_credits(self, reset_values: bool = False):
        """
        Get the credits string of the track.

        Parameters:
            - reset_values (Optional): If it should ask for the
                track information again
        """
        artists = self.get_attr("_credits", reset_values)

        return artists

    @property
    def credits(self):
        """
        Get the credits string of the track.
        """
        return self._credits

    def __repr__(self) -> str:
        return f"Apple Music Video (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Music Video (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"