from typing import Optional

from ..session.applesession import AppleSession
from ..common.exceptions import InvalidID

from .constants import AppleTypes
from .apple_item import AppleItem


class AppleGenre(AppleItem):
    def __init__(self,
                 genre_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        if not genre_id.isdigit():
            raise InvalidID(f"Genre ID Must Be Numerical")

        self._name = ""
        self._parent_name = ""
        self._parent_id = ""
        super().__init__(genre_id, AppleTypes.GENRE, session, read_data)

    def set_data(self, data: dict):
        attributes = data["attributes"]

        self._name = attributes["name"]
        self._parent_name = attributes.get("parentName", None)
        self._parent_id = attributes.get("parentId", None)

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

    def get_parent_name(self, reset_values: bool = False):
        """
        Get the name of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_parent_name", reset_values)

    @property
    def parent_name(self):
        """
        Get the name of the song.
        """
        return self._parent_name

    def get_parent_id(self, reset_values: bool = False):
        """
        Get the name of the song.

        Parameters:
            - reset_values (Optional): If it should ask for the
                song information again
        """
        return self.get_attr("_parent_id", reset_values)

    @property
    def parent_id(self):
        """
        Get the name of the song.
        """
        return self._parent_id

    @property
    def has_parent(self):
        """
        Indicates if the genre has an assigned parent genre.
        """
        return self._parent_name is not None

    def __repr__(self) -> str:
        return f"Apple Genre (Name: {self._name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Genre (Name: {self._name} | ID: {self.item_id})"
