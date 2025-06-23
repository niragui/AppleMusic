from typing import Optional

from .apple_playlist_base import ApplePlaylistBase

from .apple_track_base import AppleTrackBase

from ..session.applesession import AppleSession

PLAYLIST_IDENTIFICATOR = "pl."


class ApplePlaylist(ApplePlaylistBase):
    def __init__(self,
                 playlist_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        self._tracks = []
        super().__init__(playlist_id, session, read_data, True)

    def set_tracks(self, relationships: dict):
        self._set_relationship(relationships, "tracks", AppleTrackBase, "_tracks")

    def set_data(self,
                data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the playlist.

        Parameters:
            - data: Data given by the Apple Music API
        """
        super().set_data(data)

        relationships = data.get("relationships", None)
        if relationships is None:
            return

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
