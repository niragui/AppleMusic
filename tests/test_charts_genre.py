import pytest

from src.charts.genres_checker import is_valid_id, is_valid_name, get_genre_id, check_genre, get_genre

from src.charts.exceptions import InvalidGenre

from src.constants import API_URL, SIMPLER_API_URL, APPLE_URL

from src.session.applesession import AppleSession
from src.items.apple_genre import AppleGenre


VALID_GENRE = "Pop"
VALID_GENRE_ID = 14

INVALID_GENRE = "Fake"
INVALID_GENRE_ID = 0


def test_missing_genre():
    assert not is_valid_id(INVALID_GENRE_ID)


def test_valid_genre():
    assert is_valid_id(VALID_GENRE_ID)


def test_missing_genre_name():
    assert not is_valid_name(INVALID_GENRE)


def test_valid_genre_name():
    assert is_valid_name(VALID_GENRE)


def get_genre_id_invalid():
    with pytest.raises(InvalidGenre):
        genre_id = get_genre_id(INVALID_GENRE)


def test_get_genre_id_valid():
    genre_id = get_genre_id(VALID_GENRE)

    genre = AppleGenre(str(genre_id))

    assert genre.name == VALID_GENRE
    assert genre_id == VALID_GENRE_ID


def test_check_invalid_genre_int():
    with pytest.raises(InvalidGenre):
        check_genre(INVALID_GENRE_ID)


def test_check_invalid_genre_name():
    with pytest.raises(InvalidGenre):
        check_genre(INVALID_GENRE)


def test_check_invalid_genre_type():
    with pytest.raises(InvalidGenre):
        check_genre([123])


def test_get_genre_valid():
    genre_id = get_genre(VALID_GENRE)

    genre = AppleGenre(str(genre_id))

    assert genre.name == VALID_GENRE
    assert genre_id == VALID_GENRE_ID