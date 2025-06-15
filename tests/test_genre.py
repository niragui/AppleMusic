import pytest

from src.items.apple_genre import AppleGenre
from src.session.applesession import AppleSession

from src.common.exceptions import InvalidID

POP_ID = "14"
ALL_GENRES_ID = "34"


@pytest.fixture(scope="module")
def session():
    yield AppleSession()


def test_invalid_id(session):
    invalid_playlist = "svdvsnujvsdvsd"
    with pytest.raises(InvalidID):
        AppleGenre(invalid_playlist, session)


def test_non_existen_id(session):
    invalid_playlist = "99999"
    with pytest.raises(InvalidID):
        AppleGenre(invalid_playlist, session)


@pytest.fixture(scope="module")
def pop_genre(session):
    return AppleGenre(POP_ID, session)


@pytest.fixture(scope="module")
def all_genre(session):
    return AppleGenre(ALL_GENRES_ID, session)


def test_name(pop_genre):
    expected_name = "Pop"

    assert pop_genre.name == expected_name
    assert pop_genre.get_name() == expected_name


def test_paternity_positive(pop_genre):
    expected_name = "Music"
    expected_id = "34"

    assert pop_genre.parent_name == expected_name
    assert pop_genre.get_parent_name() == expected_name

    assert pop_genre.parent_id == expected_id
    assert pop_genre.get_parent_id() == expected_id

    assert pop_genre.has_parent


def test_paternity_negative(all_genre):
    assert all_genre.parent_name is None
    assert all_genre.get_parent_name() is None

    assert all_genre.parent_id is None
    assert all_genre.get_parent_id() is None

    assert not all_genre.has_parent