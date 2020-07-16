from ps2_census.enums import ResistType

from ps2_analysis.enums import DamageLocation, DamageTargetType
from ps2_analysis.utils import (
    all_equal,
    apply_damage_resistance,
    discover,
    float_range,
    get,
    locational_linear_falloff,
    optget,
    resolve_damage_resistance,
    resolve_health_pool,
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


def test_apply_damage_resistance():
    assert apply_damage_resistance(damage=100, resistance=0.0) == 100
    assert apply_damage_resistance(damage=100, resistance=1.0) == 0
    assert apply_damage_resistance(damage=100, resistance=1.5) == 0
    assert apply_damage_resistance(damage=100, resistance=1.5) == 0
    assert apply_damage_resistance(damage=100, resistance=0.3) == 70
    assert apply_damage_resistance(damage=101, resistance=0.3) == 71
    assert apply_damage_resistance(damage=100, resistance=-0.3) == 130


def test_locational_linear_falloff():
    assert locational_linear_falloff(0.0, 10.0, 200.0, 20.0, 100.0) == 200.0
    assert locational_linear_falloff(10.0, 10.0, 200.0, 20.0, 100.0) == 200.0
    assert locational_linear_falloff(15.0, 10.0, 200.0, 20.0, 100.0) == 150.0
    assert locational_linear_falloff(20.0, 10.0, 200.0, 20.0, 100.0) == 100.0
    assert locational_linear_falloff(30.0, 10.0, 200.0, 20.0, 100.0) == 100.0


def test_resolve_damage_resistance():
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_BASELINE,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.SMALL_ARM,
        )
        == 0.0
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_NANOWEAVE,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.SMALL_ARM,
        )
        == 0.2
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_NANOWEAVE,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.AIR_TO_GROUND_WARHEAD,
        )
        == 0.0
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_NANOWEAVE,
            damage_location=DamageLocation.HEAD,
            resist_type=ResistType.SMALL_ARM,
        )
        == 0.0
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_HEAVY_RESIST_SHIELD,
            damage_location=DamageLocation.HEAD,
            resist_type=ResistType.SMALL_ARM,
        )
        == 0.35
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_HEAVY_RESIST_SHIELD,
            damage_location=DamageLocation.LEGS,
            resist_type=ResistType.EXPLOSIVE,
        )
        == 0.35
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_FLAK_ARMOR,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.EXPLOSIVE,
        )
        == 0.5
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_FLAK_ARMOR,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.DEFAULT_ROCKET_LAUNCHER,
        )
        == 0.2
    )
    assert (
        resolve_damage_resistance(
            damage_target_type=DamageTargetType.INFANTRY_FLAK_ARMOR,
            damage_location=DamageLocation.TORSO,
            resist_type=ResistType.SMALL_ARM,
        )
        == 0.0
    )


def test_resolve_health_pool():
    assert (
        resolve_health_pool(damage_target_type=DamageTargetType.INFANTRY_BASELINE)
        == 1000
    )
    assert (
        resolve_health_pool(
            damage_target_type=DamageTargetType.INFANTRY_AUXILIARY_SHIELD
        )
        == 1050
    )
    assert (
        resolve_health_pool(
            damage_target_type=DamageTargetType.INFANTRY_HEAVY_HEALTH_SHIELD
        )
        == 1450
    )


def test_all_equal():
    assert all_equal([1, 2, 3]) is False
    assert all_equal([1, 1]) is True
    assert all_equal([]) is True
