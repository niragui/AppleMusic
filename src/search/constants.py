from enum import Enum

from ..items.apple_album_base import AppleAlbumBase
from ..items.apple_track_base import AppleTrackBase
from ..items.apple_video_base import AppleVideoBase
from ..items.apple_playlist_base import ApplePlaylistBase
from ..items.apple_artist_base import AppleArtistBase

class SearchTypes(Enum):
    ACTIVITY = "activities"
    ALBUM = "albums"
    APPLE_CURATOR = "apple-curators"
    CURATOR = "curators"
    ARTIST = "artists"
    VIDEO = "music-videos"
    PLAYLIST = "playlists"
    LABEL = "record-labels"
    TRACK = "songs"
    STATION = "stations"

BASE_SEARCH = [SearchTypes.ALBUM, SearchTypes.ARTIST, SearchTypes.PLAYLIST, SearchTypes.VIDEO, SearchTypes.TRACK]
MAX_LIMIT = 25

TYPE_CONVERTOR = {}
TYPE_CONVERTOR[SearchTypes.ALBUM] = AppleAlbumBase
TYPE_CONVERTOR[SearchTypes.TRACK] = AppleTrackBase
TYPE_CONVERTOR[SearchTypes.ARTIST] = AppleArtistBase
TYPE_CONVERTOR[SearchTypes.PLAYLIST] = ApplePlaylistBase
TYPE_CONVERTOR[SearchTypes.VIDEO] = AppleVideoBase
