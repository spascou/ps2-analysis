from ps2_analysis.utils import discover, get, optget


def test_discover():
    assert discover(data=[{"a": 1, "b": 2}]) == {".a": {1}, ".b": {2}}
    assert discover(data=[{"a": 1}, {"a": 2}]) == {".a": {1, 2}}
    assert discover(data=[{"a": {"b": 3}}]) == {".a.b": {3}}
    assert discover(data=[{"a": {"b": 3}, "c": {"d": 4}}]) == {".a.b": {3}, ".c.d": {4}}
    assert discover(data=[{"a": [{"b": 1, "c": 2, "d": 3}, {"c": 4}, {"e": 5}]}]) == {
        ".a.b": {1},
        ".a.c": {2, 4},
        ".a.d": {3},
        ".a.e": {5},
    }
    assert discover(
        data=[
            {"a": [{"b": 1, "c": 2, "d": 3}, {"c": 4}, {"e": 5}]},
            {"a": [{"b": 11, "c": 22, "d": 33}, {"c": 44}, {"e": 55}]},
            {"f": 1},
        ]
    ) == {
        ".a.b": {1, 11},
        ".a.c": {2, 22, 4, 44},
        ".a.d": {3, 33},
        ".a.e": {5, 55},
        ".f": {1},
    }


def test_get():
    assert get({"a": "1.2"}, "a", float) == 1.2


def test_optget():
    assert optget({"a": "1.2"}, "b", float) is None
    assert optget({"a": "1.2"}, "b", float, "default") == "default"
