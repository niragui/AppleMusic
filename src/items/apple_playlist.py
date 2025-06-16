from typing import Optional

import datetime

from ..common.exceptions import InvalidID

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from .apple_track_base import AppleTrackBase

from ..session.applesession import AppleSession

PLAYLIST_IDENTIFICATOR = "pl."


class ApplePlaylist(AppleItem):
    def __init__(self,
                 playlist_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        if not playlist_id.startswith(PLAYLIST_IDENTIFICATOR):
            raise InvalidID(f"Playlist ID Must Start With {PLAYLIST_IDENTIFICATOR}")

        self._name = ""
        self._full_description = ""
        self._long_description = ""

        self._artwork = None

        self._creator = ""
        self._modified_date = None

        self._tracks = []
        super().__init__(playlist_id, AppleTypes.PLAYLIST, session, read_data)

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
        self._full_description = attributes["description"]["standard"]
        self.short_description = attributes["description"].get("short", "")

        modified_date = attributes["lastModifiedDate"]

        self._modified_date = datetime.datetime.fromisoformat(modified_date[:-1])

        artwork = attributes["artwork"]
        self._artwork = ArtWork(artwork)

        self._creator = attributes["curatorName"]

        tracks_data = data["relationships"]["tracks"]

        self._tracks = []
        for track in tracks_data:
            track_id = track["id"]
            new_track = AppleTrackBase(track_id, self.session)
            new_track.set_data(track)
            self._tracks.append(new_track)

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

    @property
    def tracks(self):
        """
        Get the tracks of the playlist.
        """
        return self._tracks

    def get_tracks_amount(self, reset_values: bool = False):
        """
        Get the tracks of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        tracks = self.get_attr("_tracks", reset_values)

        return len(tracks)

    def __len__(self):
        return len(self._tracks)

    def artist_in_playlist(self, artist_id: str, reset_values: bool = False):
        """
        Checks if an artist is in a playlist.

        Parameters:
            - artist_id: ID of the artist to check
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        tracks = self.get_attr("_tracks", reset_values)

        for track in tracks:
            if track.is_by_artist(artist_id):
                return True

        return False

    def get_artist_tracks(self, artist_id: str, reset_values: bool = False):
        """
        Checks if an artist is in a playlist.

        Parameters:
            - artist_id: ID of the artist to check
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        tracks = self.get_attr("_tracks", reset_values)

        artists_tracks = []

        for track in tracks:
            if track.is_by_artist(artist_id):
                artists_tracks.append(track)

        return artists_tracks

    def get_duration(self, reset_values: bool = False):
        """
        Get the total amount of time of a playlist in miliseconds.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        if reset_values:
            self.read_data()

        total_duration = 0
        for track in self._tracks:
            total_duration += track.get_duration()

        return total_duration

    @property
    def duration(self):
        """
        Get the total amount of time of a playlist in miliseconds.
        """
        return self.get_duration()

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