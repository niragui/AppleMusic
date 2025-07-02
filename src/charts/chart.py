from typing import Optional
from urllib.parse import urlencode

from .constants import ChartsTypes
from .genres_checker import get_genre, GENRE_TYPE, ALL_GENRES
from .chart_item import AppleChartItem

from ..common.countries_handle import get_country_api_url, get_country_iso

from ..session.exceptions import ConnectionError
from ..session.applesession import AppleSession


TYPE_FIELD = "types"
GENRE_FIELD = "genre"
LIMIT_FIELD = "limit"

LIMIT_AMOUNT = 200


class AppleChart():
    def __init__(self,
                 country: str,
                 chart_type: ChartsTypes,
                 genre: GENRE_TYPE = ALL_GENRES,
                 session: Optional[AppleSession] = None) -> None:
        self.api_url = get_country_api_url(country)
        self.genre_id = get_genre(genre)

        if session is None:
            session = AppleSession()
        self.session = session

        self.country = country
        self.country_iso = get_country_iso(country)
        self.chart_type = chart_type
        self.items = []

        self.read_chart()

    def get_url(self):
        """
        Get the API request URL for the Chart
        """
        chart_url = f"{self.api_url}charts"

        params = {}
        params[TYPE_FIELD] = self.chart_type.value
        params[GENRE_FIELD] = self.genre_id
        #TODO: Check City Charts

        params[LIMIT_FIELD] = LIMIT_AMOUNT

        params_encoded = urlencode(params)

        full_url = f"{chart_url}?{params_encoded}"
        return full_url

    def set_items(self,
                   api_data: dict):
        """
        Given the API response, it loads the charts item in the class

        Parameters:
            - api_data: Dictionary with the API response
        """
        items = api_data["results"][self.chart_type.value][0]["data"]

        for pos, item in enumerate(items, 1):
            chart_item = AppleChartItem(pos, item, self.chart_type, self.session)
            self.items.append(chart_item)

    def read_chart(self):
        """
        Asks the Apple API for the charts
        """
        url = self.get_url()

        response = self.session.get(url)

        if response is None:
            raise ConnectionError(f"Could Not Read Data")

        data = response.json()

        self.set_items(data)

    def reload(self):
        """
        Asks the API for the data again
        """
        self.read_chart()

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def __repr__(self):
        return f"Apple Music Chart (Country: {self.country_iso} | Type: {self.chart_type.value} | Genre: {self.genre_id})"

    def __str__(self):
        return f"Apple Music Chart (Country: {self.country_iso} | Type: {self.chart_type.value} | Genre: {self.genre_id})"