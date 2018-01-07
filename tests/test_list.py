from poq import query


def test_get_root_as_list(fixture_list):
    result = query(".[]", fixture_list)
    assert result == fixture_list


def test_iterate_list(fixture_list):
    result = query(".[].name", fixture_list)
    assert [e["name"] for e in fixture_list] == result


def test_list_flatten(fixture_list):
    result = query(".[].numbers[]", fixture_list)
    assert [y for x in fixture_list for y in x["numbers"]] == result
