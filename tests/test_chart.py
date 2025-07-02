import pytest

from src.charts.chart import AppleChart
from src.charts.constants import ChartsTypes
from src.charts.chart_item import AppleChartItem

from src.items.apple_album_base import AppleAlbumBase
from src.items.apple_track_base import AppleTrackBase
from src.items.apple_playlist_base import ApplePlaylistBase
from src.items.apple_video_base import AppleVideoBase

from src.session.applesession import AppleSession

USA_COUNTRY = "United States of America"
CHARTS_LENGTH = 200

POP_GENRE = "Pop"


@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_length(session):
    chart = AppleChart(USA_COUNTRY, ChartsTypes.TRACKS, session=session)

    assert len(chart) == 200
    assert all([isinstance(item, AppleChartItem) for item in chart])
    assert all([isinstance(item.item, AppleTrackBase) for item in chart])


def test_genre(session):
    genre_check = "Pop"
    chart = AppleChart(USA_COUNTRY, ChartsTypes.ALBUMS, genre_check, session=session)

    for track in chart:
        assert genre_check in track._genres_names


def test_tracks_typing(session):
    chart = AppleChart(USA_COUNTRY, ChartsTypes.TRACKS, session=session)

    assert len(chart) == 200
    assert all([isinstance(item.item, AppleTrackBase) for item in chart])


def test_albums_typing(session):
    chart = AppleChart(USA_COUNTRY, ChartsTypes.ALBUMS, session=session)

    assert len(chart) == 200
    assert all([isinstance(item.item, AppleAlbumBase) for item in chart])


def test_playlist_typing(session):
    chart = AppleChart(USA_COUNTRY, ChartsTypes.PLAYLISTS, session=session)

    assert len(chart) == 200
    assert all([isinstance(item.item, ApplePlaylistBase) for item in chart])


def test_videos_typing(session):
    chart = AppleChart(USA_COUNTRY, ChartsTypes.VIDEOS, session=session)

    assert len(chart) == 200
    assert all([isinstance(item.item, AppleVideoBase) for item in chart])
