from typing import Union

from .exceptions import InvalidGenre
from .constants import GENRES

GENRE_TYPE = Union[str, int]


ALL_GENRES = "Music"


def is_valid_id(check_id: int):
    """
    Check if a genre id is a valid ID

    Parameters:
        - check_id: ID to check if valid
    """
    return check_id in GENRES.values()


def is_valid_name(check_name: str):
    """
    Check if a genre name is a valid name

    Parameters:
        - check_name: Name to check if valid
    """
    return check_name in GENRES.keys()


def get_genre_id(genre_name: str):
    """
    Returns the ID of the genre.

    Parameters:
        - genre_name: Name of the genre to return the ID
    """
    genre_id = GENRES.get(genre_name, None)

    if genre_id is None:
        raise InvalidGenre(f"Can't Find GenreId [{genre_name}]")

    return genre_id


def check_genre(genre: GENRE_TYPE):
    """
    Check if the genre is valid. If Not it raises an exception

    Parameter:
        - genre: Value to check
    """
    if isinstance(genre, str):
        if genre.isdigit():
            genre = int(genre)
        elif not is_valid_name(genre):
            raise InvalidGenre(f"Genre Name Not Found [{genre}]")
        else:
            return

    if isinstance(genre, int):
        if not is_valid_id(genre):
            raise InvalidGenre(f"Genre ID Not Found [{genre}]")
        return

    raise InvalidGenre(f"Genre Must Be String or Int [{type(genre)}]")

def get_genre(genre: GENRE_TYPE):
    """
    Returns the integer id of the genre

    Parameter:
        - genre: Value to transform to int
    """
    check_genre(genre)

    if isinstance(genre, int):
        return genre

    if genre.isdigit():
        return int(genre)

    return get_genre_id(genre)