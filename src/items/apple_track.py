from typing import Optional, Type

import datetime

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from .apple_genre import AppleGenre

from .apple_artist_base import AppleArtistBase
from .apple_track_base import AppleTrackBase
from .apple_album_base import AppleAlbumBase

from ..session.applesession import AppleSession

from .utils import get_relationship


class AppleTrack(AppleTrackBase):
    def __init__(self,
                 track_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        self._artists = []
        self._composers = []

        self._genres = []
        super().__init__(track_id, session, read_data)

    def set_genres(self, relationships: dict):
        self._set_relationship(relationships, "genres", AppleGenre, "_genres")

    def set_artists(self, relationships: dict):
        self._set_relationship(relationships, "artists", AppleArtistBase, "_artists")

    def set_composers(self, relationships: dict):
        self._set_relationship(relationships, "composers", AppleArtistBase, "_composers")

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
        self.set_genres(relationships)

    def __repr__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"