from ps2_analysis.utils import (
    discover,
    float_range,
    get,
    locational_linear_falloff,
    optget,
)


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


def test_float_range():
    assert list(float_range(start=1.0, stop=1.5, step=0.1, precision_decimals=2)) == [
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
    ]


def test_locational_linear_falloff():
    assert locational_linear_falloff(0.0, 10.0, 200.0, 20.0, 100.0) == 200.0
    assert locational_linear_falloff(10.0, 10.0, 200.0, 20.0, 100.0) == 200.0
    assert locational_linear_falloff(15.0, 10.0, 200.0, 20.0, 100.0) == 150.0
    assert locational_linear_falloff(20.0, 10.0, 200.0, 20.0, 100.0) == 100.0
    assert locational_linear_falloff(30.0, 10.0, 200.0, 20.0, 100.0) == 100.0
