from datetime import datetime
import pytest


_DICT = {
    "first_level_dict": {
        "key_1": "value_1",
        "key_2": "value_2"
    },
    "first_level_datetime": datetime(year=2018, month=1, day=10),
    "first_level_list_int": [1, 2, 3, 4, 5],
    "first_level_list_dict": [
        {
            "number": 1,
            "str": "1"
        },
        {
            "number": 2,
            "str": "2"
        },
        {
            "number": 3,
            "str": "3"
        },
        {
            "number": 4,
            "str": "4"
        },
        {
            "number": 5,
            "str": "5"
        }
    ]
}

_LIST = [
    {
        "name": "Python",
        "count": 20,
        "numbers": [1, 3, 4]
    },
    {
        "name": "Java",
        "count": 55,
        "numbers": [2, 5, 1]
    },
    {
        "name": "Scala",
        "count": 15,
        "numbers": [23, 52, 11]
    },
    {
        "name": "Javascript",
        "count": 35,
        "numbers": [8, 0, 9]
    }
]


@pytest.fixture(scope="session")
def fixture_dict():
    return _DICT


@pytest.fixture(scope="session")
def fixture_list():
    return _LIST
