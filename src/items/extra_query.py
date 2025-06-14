
from urllib.parse import urlencode

from .constants import AppleTypes, RELATIONSHIPS_PARAMS
from .exceptions import SubClassMethod

from ..constants import BASE_API_URL, SIMPLER_API_URL
from ..session.limited_request import LimitedRequest
from ..session.applesession import AppleSession

STANDARD_BATCH = 100


class AppleItemExtraQuery():
    def __init__(self,
                 item_type: AppleTypes,
                 name: str,
                 batch_size: int = STANDARD_BATCH,
                 include_params: dict = RELATIONSHIPS_PARAMS) -> None:
        self.item_type = item_type
        self.name = name

        self.batch = batch_size
        self.include_params = include_params

    def get_base_url(self,
                     item_id: str):
        """
        Get the base URL for the Extra Query

        Parameters:
            - item_id: ID of the item to get the query from
        """
        raise SubClassMethod(f"You Need To Create The get_base_url method for each extra query")

    def get_request_url(self,
                        item_id: str,
                        session: AppleSession):
        """
        Returns the limited request item for the given query

        Parameters:
            - item_id: ID of the item to get the query from
            - session: Session to use for the query
        """
        base_url = self.get_base_url(item_id)

        if len(self.include_params) > 0:
            params_encoded = urlencode(self.include_params)
            base_url = f"{base_url}?{params_encoded}"

        request = LimitedRequest(base_url, session, self.batch)

        return request

    def get_data(self,
                 item_id: str,
                 session: AppleSession):
        """
        Returns the full date for the given item

        Parameters:
            - item_id: ID of the item to get the query from
            - session: Session to use for the query
        """
        request = self.get_request_url(item_id, session)

        return request.request_full()


class AppleItemRelationshipQuery(AppleItemExtraQuery):
    def __init__(self,
                 item_type: AppleTypes,
                 name: str,
                 batch_size: int = STANDARD_BATCH,
                 include_params: dict = RELATIONSHIPS_PARAMS) -> None:
        super().__init__(item_type, name, batch_size, include_params)

    def get_base_url(self,
                     item_id: str):
        """
        Get the base URL for the Extra Query
        """
        relationship_url = f"{BASE_API_URL}{self.item_type.value}/{item_id}/{self.name}"

        return relationship_url

    def __repr__(self) -> str:
        return f"{self.item_type.value.title()}Relationship(name={self.name})"

    def __str__(self) -> str:
        return self.__repr__()


class AppleItemViewQuery(AppleItemExtraQuery):
    def __init__(self,
                 item_type: AppleTypes,
                 name: str,
                 batch_size: int = STANDARD_BATCH,
                 include_params: dict = RELATIONSHIPS_PARAMS,
                 api_url: str = BASE_API_URL) -> None:
        self.base_url = api_url
        super().__init__(item_type, name, batch_size, include_params)

    def get_base_url(self,
                     item_id: str):
        """
        Get the base URL for the Extra Query
        """
        view_url = f"{self.base_url}{self.item_type.value}/{item_id}/view/{self.name}"

        return view_url
    def __repr__(self) -> str:
        return f"{self.item_type.value.title()}View(name={self.name})"

    def __str__(self) -> str:
        return self.__repr__()


ALL_RELATIONSHIPS = []

curator_relationship = AppleItemRelationshipQuery(AppleTypes.PLAYLIST, "curator", 1)
ALL_RELATIONSHIPS.append(curator_relationship)

library_relationship = AppleItemRelationshipQuery(AppleTypes.PLAYLIST, "library")
ALL_RELATIONSHIPS.append(library_relationship)

tracks_relationship = AppleItemRelationshipQuery(AppleTypes.PLAYLIST, "tracks")
ALL_RELATIONSHIPS.append(tracks_relationship)

artists_relationship = AppleItemRelationshipQuery(AppleTypes.ALBUM, "artists", 10)
ALL_RELATIONSHIPS.append(artists_relationship)

genres_relationship = AppleItemRelationshipQuery(AppleTypes.ALBUM, "genres")
ALL_RELATIONSHIPS.append(genres_relationship)

library_relationship = AppleItemRelationshipQuery(AppleTypes.ALBUM, "library")
ALL_RELATIONSHIPS.append(library_relationship)

labels_relationship = AppleItemRelationshipQuery(AppleTypes.ALBUM, "record-labels", 10)
ALL_RELATIONSHIPS.append(labels_relationship)

tracks_relationship = AppleItemRelationshipQuery(AppleTypes.ALBUM, "tracks")
ALL_RELATIONSHIPS.append(tracks_relationship)

albums_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "albums", 10)
ALL_RELATIONSHIPS.append(albums_relationship)

artists_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "artists", 10)
ALL_RELATIONSHIPS.append(artists_relationship)

composers_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "composers", 10)
ALL_RELATIONSHIPS.append(composers_relationship)

genres_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "genres")
ALL_RELATIONSHIPS.append(genres_relationship)

library_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "library")
ALL_RELATIONSHIPS.append(library_relationship)

music_videos_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "music-videos", 10)
ALL_RELATIONSHIPS.append(music_videos_relationship)

station_relationship = AppleItemRelationshipQuery(AppleTypes.TRACK, "station")
ALL_RELATIONSHIPS.append(station_relationship)


ALL_VIEWS = []

feat_view = AppleItemViewQuery(AppleTypes.PLAYLIST, "featured-artists")
ALL_VIEWS.append(feat_view)

more_curators_view = AppleItemViewQuery(AppleTypes.PLAYLIST, "more-by-curator")
ALL_VIEWS.append(more_curators_view)

appears_on_view = AppleItemViewQuery(AppleTypes.ALBUM, "appears-on")
ALL_VIEWS.append(appears_on_view)

other_versions_view = AppleItemViewQuery(AppleTypes.ALBUM, "other-versions")
ALL_VIEWS.append(other_versions_view)

related_albums_view = AppleItemViewQuery(AppleTypes.ALBUM, "related-albums", 10, api_url=SIMPLER_API_URL)
ALL_VIEWS.append(related_albums_view)

related_videos_view = AppleItemViewQuery(AppleTypes.ALBUM, "related-videos")
ALL_VIEWS.append(related_videos_view)