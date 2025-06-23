from typing import Optional

from .apple_genre import AppleGenre

from .apple_artist_base import AppleArtistBase
from .apple_track_base import AppleTrackBase
from .apple_album_base import AppleAlbumBase
from .apple_video_base import AppleVideoBase

from ..session.applesession import AppleSession


class AppleTrack(AppleTrackBase):
    def __init__(self,
                 track_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        self._artists = []
        self._composers = []

        self._genres = []
        super().__init__(track_id, session, read_data, True)

    def set_genres(self, relationships: dict):
        self._set_relationship(relationships, "genres", AppleGenre, "_genres")

    def set_artists(self, relationships: dict):
        self._set_relationship(relationships, "artists", AppleArtistBase, "_artists")

    def set_composers(self, relationships: dict):
        self._set_relationship(relationships, "composers", AppleArtistBase, "_composers")

    def set_albums(self, relationships: dict):
        self._set_relationship(relationships, "albums", AppleAlbumBase, "_albums")

    def set_videos(self, relationships: dict):
        self._set_relationship(relationships, "music-videos", AppleVideoBase, "_videos")

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
        self.set_genres(relationships)
        self.set_composers(relationships)
        self.set_albums(relationships)
        self.set_videos(relationships)