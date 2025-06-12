from typing import Optional

from enum import Enum

import datetime
from urllib.parse import urlencode

import json

from ..session.applesession import AppleSession
from ..session.limited_request import LimitedRequest, MAX_BATCH

from .apple_item import AppleItem, AppleTypes
from .constants import RELATIONSHIPS_PARAMS

from ..constants import BASE_API_URL


class ArtistsRelationships(Enum):
    ALBUMS = "albums"
    GENRES = "genres"
    VIDEOS = "music-videos"
    PLAYLISTS = "playlists"
    STATIONS = "station"

ALL_RELATIONSHIPS = [ArtistsRelationships.ALBUMS, ArtistsRelationships.GENRES, ArtistsRelationships.VIDEOS, ArtistsRelationships.PLAYLISTS, ArtistsRelationships.STATIONS]
PLAYLISTS_BATCH = 10


class ArtistsViews(Enum):
    APPEARANCES = "appears-on-albums"
    COMPILATIOSN = "compilation-albums"
    FEATURES_ALBUMS = "featured-albums"
    FEATURES_VIDEOS = "featured-music-videos"
    FEATURES_PLAYLISTS = "featured-playlists"
    ALBUMS = "full-albums"
    LATEST = "latest-release"
    LIVE_ALBUMS = "live-albums"
    SIMILAR_ARTISTS = "similar-artists"
    SINGLES = "singles"
    TOP_VIDEOS = "top-music-videos"
    TOP_SONGS = "top-songs"

ALL_VIEWS = [ArtistsViews.APPEARANCES, ArtistsViews.COMPILATIOSN, ArtistsViews.FEATURES_ALBUMS, ArtistsViews.FEATURES_VIDEOS, ArtistsViews.FEATURES_PLAYLISTS, ArtistsViews.ALBUMS, ArtistsViews.LATEST, ArtistsViews.LIVE_ALBUMS, ArtistsViews.SIMILAR_ARTISTS, ArtistsViews.SINGLES, ArtistsViews.TOP_VIDEOS, ArtistsViews.TOP_SONGS]
LATEST_BATCH = 1


class AppleArtist(AppleItem):
    def __init__(self,
                 item_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True,
                 read_discography: bool = True):
        self.read_disc = read_discography
        self.genres = []
        self.name = ""
        self.image = ""

        self.description = ""

        self.albums = []
        self.playlists = []
        self.music_videos = []

        super().__init__(item_id, AppleTypes.ARTISTS, session, read_data)

    def set_data(self, data: dict):
        raise ValueError(f"Artists Are A Mess")

    def get_relationship(self,
                         relationship: ArtistsRelationships):
        """
        Request all the relationships of the given type and returns
        an unique list response with all the information of it.

        Parameters:
            - relationship: Relationship to request.
        """
        relationship_url = f"{BASE_API_URL}artists/{self.item_id}/{relationship.value}"

        batch = MAX_BATCH
        if relationship == ArtistsRelationships.PLAYLISTS:
            batch = PLAYLISTS_BATCH

        params_encoded = urlencode(RELATIONSHIPS_PARAMS)
        relationship_url = f"{relationship_url}?{params_encoded}"

        relationship_request = LimitedRequest(relationship_url, self.session, batch)

        return relationship_request.request_full()

    def get_view(self,
                 view: ArtistsViews):
        """
        Request all the views of the given type and returns an
        unique list response with all the information of it.
        """
        views_url = f"{BASE_API_URL}artists/{self.item_id}/view/{view.value}"

        batch = MAX_BATCH
        if view == ArtistsViews.LATEST:
            batch = LATEST_BATCH

        params_encoded = urlencode(RELATIONSHIPS_PARAMS)
        views_url = f"{views_url}?{params_encoded}"

        relationship_request = LimitedRequest(views_url, self.session, batch)

        return relationship_request.request_full()

    def read_data(self):
        """
        Asks the Apple endpoint to set the playlist data.
        """
        url = self.get_request_url()

        response = self.session.get(url)

        data = response.json()

        data = data["data"][0]

        data["relationships"] = {}
        data["views"] = {}

        for relationship in ALL_RELATIONSHIPS:
            data["relationships"][relationship.value] = self.get_relationship(relationship)

        for view in ALL_VIEWS:
            data["views"][view.value] = self.get_view(view)

        with open("artists.json", "w") as f:
            f.write(json.dumps(data, indent=4))

        self.set_data(data)

    def __repr__(self) -> str:
        return f"Apple Artist (Name: {self.name} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Artist (Name: {self.name} | ID: {self.item_id})"