from typing import Optional

from ..session.applesession import AppleSession

from .apple_item import AppleItem, AppleTypes

from .artwork import ArtWork


class AppleArtistBase(AppleItem):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = False):
        self._name = ""
        self._artwork = ""

        self._genres = []

        self._description = ""

        super().__init__(item_id, AppleTypes.ARTIST, session, read_data)

    def set_data(self, data: dict):
        attributes = data["attributes"]

        self._name = attributes["name"]

        artwork = attributes["artwork"]
        self._artwork = ArtWork(artwork)

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
        Get the name of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_name", reset_values)

    @property
    def name(self):
        """
        Get the name of the song.
        """
        return self._name

    def __repr__(self) -> str:
        return f"Apple Artist Base (Name: {self._name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Artist Base (Name: {self._name} | ID: {self.item_id})"