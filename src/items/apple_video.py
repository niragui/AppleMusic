from typing import Optional

from ..session.applesession import AppleSession
from .apple_item import AppleItem, AppleTypes

from .apple_album_base import AppleAlbumBase
from .apple_artist_base import AppleArtistBase
from .apple_track_base import AppleTrackBase
from .apple_video_base import AppleVideoBase

EXPLICIT_RATING = "explicit"


class AppleVideo(AppleVideoBase):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True):
        self._artists = []
        self._tracks = []

        super().__init__(item_id, session, read_data, True)

    def set_artists(self, relationships: dict):
        self._set_relationship(relationships, "artists", AppleArtistBase, "_artists")

    def set_tracks(self, relationships: dict):
        self._set_relationship(relationships, "songs", AppleTrackBase, "_tracks")

    def set_albums(self, relationships: dict):
        self._set_relationship(relationships, "albums", AppleAlbumBase, "_albums")

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        super().set_data(data)

        relationships = data.get("relationships", None)
        if relationships is None:
            return

        self.set_artists(relationships)
        self.set_tracks(relationships)

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