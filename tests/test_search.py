import pytest

import datetime

from src.items.apple_album_base import AppleAlbumBase
from src.items.apple_artist_base import AppleArtistBase
from src.items.apple_track_base import AppleTrackBase
from src.items.apple_playlist_base import ApplePlaylistBase

from src.search.searcher import AppleSearcher
from src.search.constants import SearchTypes
from src.search.exceptions import InvalidSearch


@pytest.fixture(scope="module")
def searcher():
    yield AppleSearcher()


def test_empty_search(searcher):
    with pytest.raises(InvalidSearch):
        searcher.search("")


def test_album_search(searcher):
    albums = searcher.search("Midnights", [SearchTypes.ALBUM])

    assert all([isinstance(album, AppleAlbumBase) for album in albums])


def test_artist_search(searcher):
    artists = searcher.search("Taylor Swift", [SearchTypes.ARTIST])

    assert all([isinstance(artist, AppleArtistBase) for artist in artists])


def test_track_search(searcher):
    tracks = searcher.search("Bejeweled", [SearchTypes.TRACK])

    assert all([isinstance(track, AppleTrackBase) for track in tracks])


def test_playlist_search(searcher):
    playlists = searcher.search("Glitter Pen", [SearchTypes.PLAYLIST])

    assert all([isinstance(playlist, ApplePlaylistBase) for playlist in playlists])
