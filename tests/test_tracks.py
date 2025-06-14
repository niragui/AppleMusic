import pytest

from src.items.apple_track import AppleTrack

from src.session.applesession import AppleSession

from src.common.exceptions import InvalidID

FORTNIGHT_TRACK_ID = "1736268216"

@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_wrong_track(session):
    invalid_track = "svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        AppleTrack(invalid_track, session)


@pytest.fixture(scope="module")
def valid_track(session):
    return AppleTrack(FORTNIGHT_TRACK_ID, session)


def test_real_track_name(valid_track):
    name = "Fortnight (feat. Post Malone)"

    test_track_name = valid_track.get_name()
    assert name == test_track_name


def test_real_track_credits(valid_track):
    real_credits = "Taylor Swift"

    test_track_credits = valid_track.get_credits()
    assert real_credits == test_track_credits
