from .constants import ChartsTypes

from ..session.applesession import AppleSession

from ..items.apple_album_base import AppleAlbumBase
from ..items.apple_track_base import AppleTrackBase
from ..items.apple_video_base import AppleVideoBase
from ..items.apple_playlist_base import ApplePlaylistBase


TYPE_CONVERTOR = {}
TYPE_CONVERTOR[ChartsTypes.ALBUMS] = AppleAlbumBase
TYPE_CONVERTOR[ChartsTypes.TRACKS] = AppleTrackBase
TYPE_CONVERTOR[ChartsTypes.PLAYLISTS] = ApplePlaylistBase
TYPE_CONVERTOR[ChartsTypes.VIDEOS] = AppleVideoBase



class AppleChartItem():
    def __init__(self,
                 position: int,
                 data: dict,
                 item_type: ChartsTypes,
                 session: AppleSession):
        self.position = position

        self.session = session

        self.item = None
        self.item_type = item_type
        self.set_item(data)

    def set_item(self,
                 data: dict):
        """
        Creates the item instance from the given data

        Parameters:
            - data: Data to set the item attributes
        """
        item_id = data["id"]

        item_class = TYPE_CONVERTOR.get(self.item_type, None)

        if item_class is None:
            raise KeyError(f"Invalid Chart Type")

        self.item = item_class(item_id, self.session, False, False)
        self.item.set_data(data)