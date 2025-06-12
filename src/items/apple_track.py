from typing import Optional


import datetime

from .apple_item import AppleItem, AppleTypes
from .artwork import ArtWork

from ..session.applesession import AppleSession
from ..constants import BASE_API_URL

class AppleTrack(AppleItem):
    def __init__(self,
                 track_id: str,
                 session: Optional[AppleSession] = None,
                 read_data: bool = True) -> None:
        self.name = ""
        self.credits = ""
        self.artists = []
        self.composer = ""

        self.album_name = ""
        self.album_id = ""
        self.album_position = 0
        self.album_disc = 0

        self.genres = []
        self.duration = 0
        self.release = None

        self.artwork = None
        super().__init__(track_id, AppleTypes.TRACK, session, read_data)

    def set_data(self,
                 data: dict):
        """
        Given the data from the Apple Music API,
        it set the content of the track.

        Parameters:
            - data: Data given by the Apple Music API
        """
        attributes = data["attributes"]

        self.name = attributes["name"]
        self.credits = attributes["artistName"]
        self.composer = attributes.get("composerName", "")

        self.album_name = attributes["albumName"]
        self.album_position = attributes["trackNumber"]
        self.album_disc = attributes["discNumber"]

        artwork = attributes["artwork"]
        self.artwork = ArtWork(artwork)

        self.genres = attributes["genreNames"]
        self.duration = attributes.get("durationInMillis", 0)

        release_str = attributes.get("releaseDate", None)
        if release_str:
            self.release = datetime.date.fromisoformat(release_str)
        else:
            self.release = None

        url = attributes["url"]
        album_id_start = url.rfind("/") + 1
        album_id_end = url.find("?", album_id_start)

        self.album_id = url[album_id_start: album_id_end]

        relations = data.get("relationships", None)
        if relations is None:
            return

        artists = relations["artists"]["data"]
        self.artists = []
        for artist in artists:
            self.artists.append(artist["id"])

    def get_image(self,
                  width: Optional[int] = None,
                  height: Optional[int] = None):
        """
        Returns the url of the image for the artwork

        Parameters:
            - width: Width to use. If None, the max possible will be used
            - height: Height to use. If None, the max possible will be used
        """
        return self.artwork.get_image(width, height)

    def get_duration(self, reset_values: bool = False):
        """
        Get the duration of the playlist.

        Parameters:
            - reset_values (Optional): If it should ask for the
                playlist information again
        """
        return self.get_attr("duration", reset_values)

    def __repr__(self) -> str:
        return f"Apple Track (Name: {self.name} | Credits: {self.credits} | ID: {self.item_id})"

    def __str__(self) -> str:
        return f"Apple Track (Name: {self.name} | Credits: {self.credits} | ID: {self.item_id})"