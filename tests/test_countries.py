import pytest

from src.common.countries_handle import get_country_iso, get_country_api_url, get_country_base_url
from src.common.exceptions import MissingCountry, InvalidCountry

from src.constants import API_URL, SIMPLER_API_URL, APPLE_URL

USA = "United States of America"

VALID_COUNTRY = "Argentina"
VALID_ISO = "AR"
NO_APPLE_COUNTRY = "Faroe Islands"
INVALID_COUNTRY = "Non Existing"


def test_missing_country():
    with pytest.raises(MissingCountry):
        iso_code = get_country_iso(INVALID_COUNTRY)


def test_no_apple():
    with pytest.raises(InvalidCountry):
        iso_code = get_country_iso(NO_APPLE_COUNTRY)


def test_valid_country():
    iso_code = get_country_iso(VALID_COUNTRY)

    assert iso_code == VALID_ISO


def test_api_url():
    api_url = get_country_api_url(USA)

    assert api_url.lower() == SIMPLER_API_URL.lower()


def test_complex_api_url():
    complex_api_url = get_country_api_url(USA, False)

    assert complex_api_url.lower() == API_URL.lower()


def test_base_apple_url():
    complex_apple_url = get_country_base_url(USA)

    assert complex_apple_url.lower() == APPLE_URL.lower()