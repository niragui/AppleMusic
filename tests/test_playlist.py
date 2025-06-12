import pytest

from src.items.apple_playlist import ApplePlaylist
from src.session.applesession import AppleSession

from src.common.exceptions import InvalidID

TOP_GLOBAL_ID = "pl.d25f5d1181894928af76c85c967f8f31"


@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_wrong_format(session):
    invalid_playlist = "svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        ApplePlaylist(invalid_playlist, session)


def test_wrong_playlist(session):
    invalid_playlist = "pl.svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        ApplePlaylist(invalid_playlist, session)


@pytest.fixture(scope="module")
def valid_playlist(session):
    return ApplePlaylist(TOP_GLOBAL_ID, session)


def test_real_playlist_name(valid_playlist):
    name = "Top 100: Global"
    test_playlist_name = valid_playlist.get_name()
    assert name == test_playlist_name
    assert valid_playlist.name == name


def test_real_playlist_length(valid_playlist):
    total_length = 100
    test_playlist_length = valid_playlist.get_tracks_amount()
    assert total_length == test_playlist_length
    assert len(valid_playlist) == total_length


def test_real_playlist_owner(valid_playlist):
    owner = "Apple Music"
    test_playlist_owner = valid_playlist.get_owner()
    assert owner == test_playlist_owner
    assert valid_playlist.owner == owner

