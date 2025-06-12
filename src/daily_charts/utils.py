from .exceptions import InvalidID
from .constants import MATCHING_VALUES_LENGTH


RECORD_ID_SEPARATOR = " By: "


def construct_record_id(record_title: str,
                        record_credits: str):
    """
    Given a record information, it returns a string
    representing the record uniquely

    Parameters:
        - record_title: Title of the record
        - record_credits: Credits of the record
    """
    record_id = record_title
    record_id += RECORD_ID_SEPARATOR
    record_id += record_credits

    return record_id


def split_record_id(record_id: str):
    """
    Given a record id, it returns a list with the title
    and the credits separated

    Parameters:
        - record_id: ID to split
    """
    if record_id.find(RECORD_ID_SEPARATOR) < 0:
        raise InvalidID(f"A Record ID Must Include A Valid Separator [{record_id}]")

    data = record_id.split(RECORD_ID_SEPARATOR)

    if len(data) < MATCHING_VALUES_LENGTH:
        raise InvalidID(f"A Record ID Must Include A Valid Separator [{record_id}]")

    if len(data) > MATCHING_VALUES_LENGTH:
        raise InvalidID(f"A Record ID Must Include Only One Valid Separator [{record_id}]")

    return data