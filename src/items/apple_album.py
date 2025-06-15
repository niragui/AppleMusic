from typing import Optional, TYPE_CHECKING

import datetime

from ..session.applesession import AppleSession
from .apple_item import AppleItem, AppleTypes

if TYPE_CHECKING:
    from .apple_track import AppleTrack

from .artwork import ArtWork

EXPLICIT_RATING = "explicit"


class AppleAlbum(AppleItem):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True):
        self._name = ""
        self._credits = ""
        self._artists = []

        self._tracks = []

        self._tag = ""
        self._long_desc = ""
        self._short_desc = ""

        self._explicit = False
        self._single = False
        self._compilation = False
        self._complete = False

        self._artwork = None

        self._labels = []
        self._release_date = None
        self._genres = []
        super().__init__(item_id, AppleTypes.ALBUM, session, read_data)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        attributes = data["attributes"]
        relations = data["relationships"]

        self._name = attributes["name"]
        self._credits = attributes["artistName"]

        edit_notes = attributes["editorialNotes"]
        self._tag = edit_notes.get("tagline", "")
        self._short_desc = edit_notes.get("short", "")
        self._long_desc = edit_notes.get("standard", "")

        content = attributes["contentRating"]
        self._explicit = content == EXPLICIT_RATING
        self._single = attributes["isSingle"]
        self._compilation = attributes["isCompilation"]
        self._complete = attributes["isComplete"]

        artists = relations["artists"]
        self._artists = []
        for artist in artists:
            self._artists.append(artist["id"])

        label = attributes["recordLabel"]
        self._labels = label.split(" / ")

        artwork = attributes["artwork"]
        self._artwork = ArtWork(artwork)

        self._genres = attributes["genreNames"]

        date_str = attributes["releaseDate"]
        self._release_date = datetime.date.fromisoformat(date_str)

        tracks = relations["tracks"]
        self._tracks = []
        for track in tracks:
            track_id = track["id"]
            new_track = AppleTrack(track_id, self.session, False)
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
        return self.get_attr("_long_desc", reset_values)

    @property
    def description(self):
        """
        Get the description of the playlist.
        """
        return self._long_desc

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
        return f"Apple Album (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Album (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"