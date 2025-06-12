import pytest

import datetime

from src.items.apple_album import AppleAlbum
from src.session.applesession import AppleSession

from src.common.exceptions import InvalidID

MIDNIGHTS_ID = "1649434004"


@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_wrong_format(session):
    invalid_playlist = "svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        AppleAlbum(invalid_playlist, session)


@pytest.fixture(scope="module")
def valid_album(session):
    yield AppleAlbum(MIDNIGHTS_ID, session)


def test_real_album_name(valid_album):
    name = "Midnights"
    test_album_name = valid_album.get_name()

    assert name == test_album_name
    assert name == valid_album.name


def test_real_album_credits(valid_album):
    credits = "Taylor Swift"
    test_album_credits = valid_album.get_credits()

    assert credits == test_album_credits
    assert credits == valid_album.credits


def test_real_album_length(valid_album):
    test_album_length = valid_album.get_tracks_amount()
    real_album_length = 14

    assert real_album_length == test_album_length
    assert len(valid_album) == real_album_length


def test_real_album_release_date(valid_album):
    release_date = datetime.date(2022, 10, 21)
    test_release_date = valid_album.get_release_date()

    assert release_date == test_release_date


def test_real_album_duration(valid_album):
    real_duration_min = 2655000
    real_duration_max = 2657000
    test_duration = valid_album.get_duration()

    assert test_duration > real_duration_min
    assert test_duration < real_duration_max