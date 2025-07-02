from typing import Optional, List

from enum import Enum

import json

from urllib.parse import urlencode

from .exceptions import InvalidSearch
from .constants import SearchTypes, TYPE_CONVERTOR, MAX_LIMIT, BASE_SEARCH

from ..session.applesession import AppleSession
from ..constants import API_URL

TOP_RESULTS_KEY = "topResults"

class AppleSearcher():
    def __init__(self,
                 session: Optional[AppleSession] = None):
        if session is None:
            session = AppleSession()

        self.session = session

    def get_url(self,
                search_term: str,
                types: Optional[List[SearchTypes]] = None,
                limit: int = MAX_LIMIT):
        """
        Creates the APÏ url for searching

        Parameters:
            - search_term: Term to search for
            - types: Types to accept in the search
            - limit: Amount of instances to ask for
        """
        if types is None:
            types = BASE_SEARCH

        if limit > MAX_LIMIT:
            raise ValueError(f"Limit Must Be {MAX_LIMIT} at most [{limit}]")

        if limit <= 0:
            raise ValueError(f"Limit Must Be A Positive Integer [{limit}]")

        url = f"{API_URL}search"

        params = {}
        params["types"] = ",".join([search_type.value for search_type in types])
        params["term"] = search_term
        params["limit"] = limit
        params["with"] = "topResults"

        params_encoded = urlencode(params)

        url = f"{url}/?{params_encoded}"

        return url

    def parse_item(self,
                   item_data: dict):
        """
        Parses the JSON of one item into an item class

        Parameters:
            - item: Dictionary of the item to parse
        """
        result_type = SearchTypes(item_data["type"])
        create_class = TYPE_CONVERTOR.get(result_type, None)
        if create_class is None:
            raise InvalidSearch(f"Invalid Search Type [{result_type.value}]")

        item_id = item_data["id"]
        item = create_class(item_id, self.session, False, False)
        item.set_data(item_data)

        return item

    def parse_response(self,
                       data: dict,
                       types: List[SearchTypes]):
        """
        Parses the JSON from the API response into a list of
        items.

        Parameters:
            - data: Dictionary of the API response
        """
        results = data["results"]
        search_results = []

        added_ids = []

        for key, results_dict in results.items():
            for item_result in results_dict["data"]:
                item = self.parse_item(item_result)
                if item.item_id in added_ids:
                    continue
                added_ids.append(item.item_id)
                search_results.append(item)

        return search_results

    def search(self,
               search_term: str,
               types: Optional[List[SearchTypes]] = None,
               limit: int = MAX_LIMIT):
        """
        Asks the API for the search term.

        Parameters:
            - search_term: Term to search for
            - types: Types to accept in the search
            - limit: Amount of instances to ask for
        """
        if len(search_term) == 0:
            raise InvalidSearch("Search Term Can't Be Empty")

        url = self.get_url(search_term, types, limit)

        if types is None:
            types = BASE_SEARCH

        response = self.session.get(url)

        if response is None:
            raise InvalidSearch("Could Not Achieve Asked Search")

        data = response.json()

        return self.parse_response(data, types)
