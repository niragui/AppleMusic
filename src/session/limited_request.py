from typing import Optional

from .applesession import AppleSession


MAX_BATCH = 100

LIMIT_FIELD = "limit"
OFFSET_FIELD = "offset"


class LimitedRequest():
    def __init__(self,
                 base_url: str,
                 session: Optional[AppleSession] = None,
                 batch: int = MAX_BATCH,
                 limit_field: str = LIMIT_FIELD,
                 offset_field: str = OFFSET_FIELD) -> None:
        if batch > MAX_BATCH:
            raise ValueError(f"Batch Can't Be Over {MAX_BATCH} [{batch}]")

        if batch <= 0:
            raise ValueError(f"Batch Must Be A Positive Integer [{batch}]")

        if session is None:
            session = AppleSession()

        self.base_url = base_url
        self.has_params = base_url.find("?") > 0
        self.batch = batch
        self.session = session
        self.limit_field = limit_field
        self.offset_field = offset_field

    def get_url(self,
                offset: int = 0):
        """
        Creates the URL for the the request

        Parameters:
            - offset: Offset to use in the url
        """
        if not self.has_params:
            offset_link = f"{self.base_url}?"
        else:
            offset_link = f"{self.base_url}&"

        offset_link += f"{self.offset_field}={offset}&{self.limit_field}={self.batch}"

        return offset_link

    def get_data(self,
                 offset: int):
        """
        Asks the API for the data for the given offset
        """
        amount_link = self.get_url(offset)
        response = self.session.get(amount_link)
        if response is None:
            return {"data": []}

        data = response.json()
        return data

    def request_full(self):
        """
        Iterates till completion of the elements
        """
        all_data = []

        data = self.get_data(len(all_data))
        while "next" in data:
            all_data.extend(data["data"])
            data = self.get_data(len(all_data))

        all_data.extend(data["data"])

        return all_data
