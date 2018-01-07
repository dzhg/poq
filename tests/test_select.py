from poq import query


def test_select_eq_int(fixture_list):
    result = query(".[] | select(.count == 20)", fixture_list)
    assert 2 == len(result)
    assert 20 == result[0]["count"]
    assert "Python" == result[0]["name"]
    assert 20 == result[1]["count"]
    assert "Scala" == result[1]["name"]


def test_select_eq_str(fixture_list):
    result = query('.[] | select(.name == "Python")', fixture_list)
    assert 1 == len(result)
    assert "Python" == result[0]["name"]
