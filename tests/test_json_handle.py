import pytest

import os

import datetime

from src.common.json_handle import read_json, write_json


THIS_DIRECTORY = os.path.dirname(__file__)
TEST_DATA_FOLDER = os.path.join(THIS_DIRECTORY, "test_cases")

MISSING_FILE = os.path.join(TEST_DATA_FOLDER, "missing_file.json")
WRONG_FILE = os.path.join(TEST_DATA_FOLDER, "wrong.json")
CORRECT_FILE = os.path.join(TEST_DATA_FOLDER, "correct.json")
WRITE_FILE = os.path.join(TEST_DATA_FOLDER, "save.json")


VALID_DICT = {"case": "correct"}
INVALID_DICT = {"date": datetime.date(2025, 9, 10)}


def test_wrong_path_read():
    data = read_json(MISSING_FILE)

    assert len(data) == 0
    assert isinstance(data, dict)


def test_wrong_path_read_none():
    data = read_json(MISSING_FILE, None)

    assert data is None


def test_wrong_format():
    data = read_json(WRONG_FILE, None)

    assert data is None


def test_correct_case():
    data = read_json(CORRECT_FILE)

    assert len(data) == 1
    assert isinstance(data, dict)


def test_write_wrong():
    with pytest.raises(TypeError):
        write_json(WRITE_FILE, INVALID_DICT)


def test_write_correct():
    write_json(WRITE_FILE, VALID_DICT)

    saved_data = read_json(WRITE_FILE)

    assert len(saved_data) == len(VALID_DICT)
    assert type(saved_data) == type(VALID_DICT)
    for key, value in VALID_DICT.items():
        saved_value = saved_data.get(key, datetime.date.today())
        assert saved_value == value