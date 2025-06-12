from typing import Optional

from ..session.applesession import AppleSession
from ..session.limited_request import LimitedRequest
from ..constants import BASE_APPLE_URL, BASE_API_URL

from .exceptions import SubClassMethod
from .constants import AppleTypes
from .extra_query import ALL_VIEWS, ALL_RELATIONSHIPS


URL_CONVERSOR = {}
URL_CONVERSOR[AppleTypes.PLAYLIST] = "playlist"
URL_CONVERSOR[AppleTypes.TRACK] = "song"
URL_CONVERSOR[AppleTypes.ALBUM] = "album"
URL_CONVERSOR[AppleTypes.ARTISTS] = "artist"
URL_CONVERSOR[AppleTypes.VIDEOS] = "music-video"


class AppleItem():
    def __init__(self,
                 item_id: str,
                 item_type: AppleTypes,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True):
        self.item_id = item_id
        self.item_type = item_type
        if session is None:
            session = AppleSession()
        self.session = session

        self.relationships = []
        for relationship in ALL_RELATIONSHIPS:
            if relationship.item_type == self.item_type:
                self.relationships.append(relationship)

        self.views = []
        for view in ALL_VIEWS:
            if view.item_type == self.item_type:
                self.views.append(view)

        if read_data:
            self.read_data()

    def set_data(self,
                 data: dict):
        """
        Sets the parameters from the API response.

        Parameters:
            - data: Dictionary response gotten from the API
        """
        raise SubClassMethod(f"set_data Needs To Be Created For Each Class")

    def get_url(self):
        """
        Returns the URL to acces the item via web browser
        """
        url_type = URL_CONVERSOR.get(self.item_type, None)

        if url_type is None:
            raise TypeError(f"Invalid Item Type [{self.item_type}]")

        return f"{BASE_APPLE_URL}/{url_type}/useless/{self.item_id}"

    def get_request_url(self):
        """
        Creates The URL to request the data for the given item
        """
        url = f"{BASE_API_URL}{self.item_type.value}/{self.item_id}"

        return url

    def read_data(self):
        """
        Asks the Apple endpoint to set the playlist data.
        """
        url = self.get_request_url()

        response = self.session.get(url)

        if response is None:
            raise ConnectionError(f"Could Not Read Data")

        data = response.json()
        data = data["data"][0]

        data["relationships"] = {}
        data["views"] = {}

        for relationship in self.relationships:
            data["relationships"][relationship.name] = relationship.get_data(self.item_id, self.session)

        for view in self.views:
            data["relationships"][view.name] = view.get_data(self.item_id, self.session)

        self.set_data(data)

    def get_attr(self, attr_name: str, reset_values: bool = False):
        """
        Get an attribute of the item.

        Parameters:
            - attr_name: Name of the attribute to retrieve
            - reset_values (Optional): If it should ask for the
                album information again
        """
        if reset_values:
            self.read_data()

        if not hasattr(self, attr_name):
            raise Exception(f"{self} Item Does Not Have A {attr_name} Attribute")

        return getattr(self, attr_name)

