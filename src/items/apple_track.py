from typing import Optional


import datetime

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from .apple_genre import AppleGenre
from .apple_artist_base import AppleArtistBase
from .apple_track_base import AppleTrackBase

from ..session.applesession import AppleSession


def get_relationship(relationships: dict,
                     relationship_name: str):
    """
    Extract the data inside a relationship.
    Returns None if not found

    Parameters:
        - relationships: Dictionary with all the relationships
        - relationship_name: Name of the relationship to extract
    """
    searched_relation = relationships.get(relationship_name, None)
    if searched_relation is None:
        return None

    if "data" in searched_relation:
        searched_relation = searched_relation["data"]

    return searched_relation


class AppleTrack(AppleTrackBase):
    def __init__(self,
                 track_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        self._artists = []
        self._composers = []

        self._genres = []
        super().__init__(track_id, session, read_data)

    def set_genres(self, relationships: dict):
        """
        Sets the artist data given the relationships dictionary.

        Parameters:
            - relationships: Dictionary with the track relationships
        """
        genres = get_relationship(relationships, "genres")
        if genres is None:
            return

        self._genres = []

        for genre in genres:
            genre_id = genre["id"]
            genre_item = AppleGenre(genre_id, self.session, False)
            genre_item.set_data(genre)

            self._genres.append(genre_item)

    def set_artists(self, relationships: dict):
        """
        Sets the artists data given the relationships dictionary.

        Parameters:
            - relationships: Dictionary with the track relationships
        """
        self._artists = []

        artists = get_relationship(relationships, "artists")
        if artists is None:
            return

        for artist in artists:
            artist_id = artist["id"]
            artist_item = AppleArtistBase(artist_id, self.session)
            artist_item.set_data(artist)

            self._artists.append(artist_item)

    def set_composers(self, relationships: dict):
        self._composers = []

        composers = get_relationship(relationships, "composers")
        if composers is None:
            return

        for composer in composers:
            composer_id = composer["id"]
            composer_item = AppleArtistBase(composer_id, self.session)
            composer_item.set_data(composer)

            self._composers.append(composer_item)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        super().set_data(data)

        relationships = data.get("relationships", None)
        if relationships is None:
            return

        self.set_artists(relationships)
        self.set_genres(relationships)

    def __repr__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Track (Name: {self._name} | Credits: {self._credits} | ID: {self.item_id})"