from typing import Optional

import datetime

from ..common.exceptions import InvalidID

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from .apple_track_base import AppleTrackBase

from ..session.applesession import AppleSession

PLAYLIST_IDENTIFICATOR = "pl."


class ApplePlaylistBase(AppleItem):
    def __init__(self,
                 playlist_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True,
                 read_extra: bool = False) -> None:
        if not playlist_id.startswith(PLAYLIST_IDENTIFICATOR):
            raise InvalidID(f"Playlist ID Must Start With {PLAYLIST_IDENTIFICATOR}")

        self._name = ""
        self._full_description = ""
        self._long_description = ""

        self._artwork = None

        self._creator = ""
        self._modified_date = None

        super().__init__(playlist_id, AppleTypes.PLAYLIST, session, read_data, read_extra)

    def set_data(self,
                data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the playlist.

        Parameters:
            - data: Data given by the Apple Music API
        """

        attributes = data["attributes"]

        self._name = attributes["name"]

        description = attributes.get("description", {})
        self._full_description = description.get("standard", "")
        self.short_description = description.get("short", "")

        modified_date = attributes["lastModifiedDate"]

        self._modified_date = datetime.datetime.fromisoformat(modified_date[:-1])

        artwork = attributes["artwork"]
        self._artwork = ArtWork(artwork)

        self._creator = attributes["curatorName"]

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
        return self.get_attr("_full_description", reset_values)

    @property
    def description(self):
        """
        Get the description of the playlist.
        """
        return self._full_description

    def get_tracks(self, amount: Optional[int] = None, reset_values: bool = False):
        """
        Get the tracks of the playlist.

        Parameters:
            - amount (Optional): Amount of tracks to get. Playlist order
                will be respected. If none or negative, all tracks will
                be returned. By default at None.
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        tracks = self.get_attr("_tracks", reset_values)

        if amount is None:
            return tracks
        elif amount <= 0 or len(tracks) <= amount:
            return tracks
        else:
            return tracks[:amount]

    def get_owner(self, reset_values: bool = False):
        """
        Get the owner name of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("_creator", reset_values)

    @property
    def owner(self):
        """
        Get the owner name of the playlist.
        """
        return self._creator

    def __repr__(self) -> str:
        return f"Apple Playlist (Name: {self._name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Playlist (Name: {self._name} | ID: {self.item_id})"