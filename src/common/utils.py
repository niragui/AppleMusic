
import os

from ..constants import DATA_FOLDER
from ..constants import BASE_APPLE_URL, BASE_API_URL, BASE_SIMPLER_API_URL

from .json_handle import read_json
from .exceptions import MissingCountry, InvalidCountry

COUNTRIES_FILE = os.path.join(DATA_FOLDER, "countries.json")
COUNTRIES = read_json(COUNTRIES_FILE, {})

HAS_APPLE_FIELD  = "has_apple"
ISO_CODE_FIELD = "alpha-2"


def get_country_iso(country: str):
    """
    Gets the ISO-2 code of am apple-supported country

    Parameters:
        - country: Name of the conuntry to check for
    """
    found_country = COUNTRIES.get(country, None)

    if found_country is None:
        raise MissingCountry(f"Country Was Not Found [{country}]")

    has_apple = found_country.get(HAS_APPLE_FIELD, False)
    iso_code = found_country.get(ISO_CODE_FIELD, None)

    if iso_code is None:
        raise InvalidCountry(f"Country Missing ISO Code [{country}]")

    if not has_apple:
        raise InvalidCountry(f"Country Isn't Supported by Apple [{country}]")

    return iso_code


def get_country_api_url(country: str,
                        simple_api: bool = True):
    """
    Creates the URL of the API for the asked country

    Parameters:
        - country: Country Name
        - simple_api: Bool indicating if it should be the standard api or the AMP one
    """
    iso_code = get_country_iso(country)

    start_url = BASE_API_URL
    if simple_api:
        start_url = BASE_SIMPLER_API_URL

    api_url = f"{start_url}{iso_code}/"

    return api_url


def get_country_base_url(country: str):
    """
    Creates the URL of the API for the asked country

    Parameters:
        - country: Country Name
        - simple_api: Bool indicating if it should be the standard api or the AMP one
    """
    iso_code = get_country_iso(country)

    api_url = f"{BASE_APPLE_URL}{BASE_API_URL}/"

    return api_url