from typing import Optional, TYPE_CHECKING

from enum import Enum

from ..session.applesession import AppleSession

from .apple_artist_base import AppleArtistBase



class AppleArtist(AppleArtistBase):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True,
                 read_discography: bool = True):
        self.read_disc = read_discography

        self._albums = []
        self._playlists = []
        self._music_videos = []

        super().__init__(item_id, session, read_data)

    def set_data(self, data: dict):
        super().set_data(data)

    def __repr__(self) -> str:
        return f"Apple Artist (Name: {self._name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Artist (Name: {self._name} | ID: {self.item_id})"