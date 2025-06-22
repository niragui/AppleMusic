import pytest

from src.items.apple_video import AppleVideo

from src.session.applesession import AppleSession

from src.common.exceptions import InvalidID

BEJEWELED_VIDEO_ID = "1651347213"

@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_wrong_video(session):
    invalid_video = "svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        AppleVideo(invalid_video, session)


@pytest.fixture(scope="module")
def valid_track(session):
    return AppleVideo(BEJEWELED_VIDEO_ID, session)


def test_real_track_name(valid_track):
    name = "Bejeweled"

    test_track_name = valid_track.get_name()
    assert name == test_track_name


def test_real_track_credits(valid_track):
    real_credits = "Taylor Swift"

    test_track_credits = valid_track.get_credits()
    assert real_credits == test_track_credits
