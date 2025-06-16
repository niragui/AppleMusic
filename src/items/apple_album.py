from typing import Optional

import datetime

from ..session.applesession import AppleSession
from .apple_item import AppleItem, AppleTypes

from .apple_album_base import AppleAlbumBase

from .artwork import ArtWork

EXPLICIT_RATING = "explicit"


class AppleAlbum(AppleAlbumBase):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True):
        super().__init__(item_id, session, read_data)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        super().set_data(data)

    def __repr__(self) -> str:
        return f"Apple Album (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Album (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"