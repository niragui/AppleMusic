from typing import Optional

from .chart_record import DailyChartRecord
from .playlists_endpoint import read_countries_playlists
from .exceptions import InvalidCountry

from ..session.applesession import AppleSession


class DailyChartWebsite():
    def __init__(self,
                 country: str,
                 session: Optional[AppleSession] = None) -> None:
        self.entries = []
        if session is None:
            session = AppleSession()

        self.url = None
        self.country = country.title()
        self.session = session

        self.set_url()

    def set_url(self):
        """
        Sets the URL for the asked country
        """
        playlists = read_countries_playlists(self.session)

        url = playlists.get(self.country, None)

        if url is None:
            raise InvalidCountry(f"Can't Retrieve Charts From {self.country}")

        self.url = url

    def read_entries(self):
        """
        Asks the Apple API for the entries in the chart
        """