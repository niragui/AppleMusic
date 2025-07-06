
from ..constants import BASE_APPLE_URL, BASE_API_URL, BASE_SIMPLER_API_URL

from .exceptions import MissingCountry, InvalidCountry
from .constants import COUNTRIES


HAS_APPLE_FIELD  = "has_apple"
ISO_CODE_FIELD = "alpha-2"

BASE_FLAG_URL = "https://flagcdn.com/w320/"


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
        - simple_api: Bool indicating if it should be the standard api
            or the AMP one
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
    """
    iso_code = get_country_iso(country)

    api_url = f"{BASE_APPLE_URL}{iso_code}/"

    return api_url


def get_country_flag_iso(country_iso: str):
    """
    Creates the URL of the flag given the iso

    Parameters:
        - country: ISO of the country to get the flag from
    """
    country_iso = country_iso.lower()

    return f"{BASE_FLAG_URL}{country_iso}.png"


def get_country_flag(country: str):
    """
    Creates the URL of the flag given the name

    Parameters:
        - country: Name of the country to get the flag from
    """
    iso_code = get_country_iso(country)

    return get_country_flag_iso(iso_code)
