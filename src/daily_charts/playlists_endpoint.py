from ..session.applesession import AppleSession
from ..session.exceptions import ConnectionError

from .constants import BASE_PLAYLIST, BASE_NAME

LIMIT_FIELD = "LIMIT_HERE"
OFFSET_FIELD = "OFFSET_HERE"

MAX_LIMIT = 200
MAX_OFFSET = 200

RESULTS_FIELD = "results"
CHARTS_FIELD = "dailyGlobalTopCharts"
DATA_FIELD = "data"
ATTRIBUTES_FIELD = "attributes"
URL_FIELD = "url"
NAME_FIELD = "name"

BASE_URL = f"https://amp-api.music.apple.com/v1/catalog/us/charts?chartId=119&limit={LIMIT_FIELD}&offset={OFFSET_FIELD}"


class PlaylistEndpoint():
    def __init__(self,
                 limit: int = MAX_LIMIT,
                 offset: int = 0) -> None:
        if limit > MAX_LIMIT:
            raise ValueError(f"Limit Can't Be Over {MAX_LIMIT}")
        if limit <= 0:
            raise ValueError(f"Limit Must Be A Positive Value")

        if offset >= MAX_OFFSET:
            raise ValueError(f"Offset Can't Be Over {MAX_OFFSET}")
        if offset < 0:
            raise ValueError(f"Offset Must Be At Least 0")

        self.limit = limit
        self.offset = offset

    def get_url(self):
        """
        Returns the formatted URL for the endpoint
        """
        url = BASE_URL
        url = url.replace(LIMIT_FIELD, str(self.limit))
        url = url.replace(OFFSET_FIELD, str(self.offset))

        return url


def get_playlists_endpoint(limit: int = MAX_LIMIT,
                           offset: int = 0):
    """
    Creates the URL for the top charts playlists

    Parameters:
        - limit: How many playlists to retrieve
        - offset: Where to start from
    """
    endpoint = PlaylistEndpoint(limit, offset)

    return endpoint.get_url()


def read_countries_playlists(session: AppleSession):
    """
    Read all the endpoints for each country

    Returns a dictionary of {country: id}
    """
    endpoint = get_playlists_endpoint()

    response = session.get(endpoint)

    data = response.json()

    results = data.get(RESULTS_FIELD, None)
    if results is None:
        raise ConnectionError(f"Could Not Read Playlists From Response")

    charts = results.get(CHARTS_FIELD, None)
    if charts is None or len(charts) == 0:
        raise ConnectionError(f"Could Not Read Charts From Results")

    charts = charts[0].get(DATA_FIELD, None)
    if charts is None:
        raise ConnectionError(f"Could Not Read Charts From Results")

    playlists = {}
    for country in charts:
        attributes = country.get(ATTRIBUTES_FIELD, None)
        if attributes is None:
            raise ConnectionError(f"Could Not Read Attributes From Country")

        url = attributes.get(URL_FIELD, None)
        url_id = url.replace(BASE_PLAYLIST, "")

        name = attributes.get(NAME_FIELD, None)
        country = name.replace(BASE_NAME, "")
        country = country.title()

        playlists[country] = url_id

    return playlists
