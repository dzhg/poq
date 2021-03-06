from poq import query


def test_get_root(fixture_dict):
    result = query(".", fixture_dict)
    assert result == fixture_dict


def test_get_first_level_child_as_dict(fixture_dict):
    result = query(".first_level_dict", fixture_dict)
    assert result == fixture_dict["first_level_dict"]


def test_get_first_level_child_none(fixture_dict):
    result = query(".missing_one", fixture_dict)
    assert result is None


def test_get_second_level_child(fixture_dict):
    result = query(".first_level_dict.key_1", fixture_dict)
    assert result == "value_1"


def test_get_second_level_child_list(fixture_dict):
    result = query(".first_level_list_int[]", fixture_dict)
    assert result == fixture_dict["first_level_list_int"]


def test_get_second_level_child_list_dict_field(fixture_dict):
    result = query(".first_level_list_dict[].number", fixture_dict)
    assert result == [x["number"] for x in fixture_dict["first_level_list_dict"]]
