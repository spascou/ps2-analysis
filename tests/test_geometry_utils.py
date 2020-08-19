import math

from ps2_analysis.fire_groups.damage_profile import DamageLocation
from ps2_analysis.geometry_utils import planetman_hit_location, random_point_in_disk


def test_planetman_hit_location():
    assert (
        planetman_hit_location(x=0.0, y=0.0, aim_location=DamageLocation.HEAD)
        == DamageLocation.HEAD
    )
    assert (
        planetman_hit_location(x=0.0, y=0.0, aim_location=DamageLocation.TORSO)
        == DamageLocation.TORSO
    )
    assert (
        planetman_hit_location(x=0.0, y=0.0, aim_location=DamageLocation.LEGS)
        == DamageLocation.LEGS
    )


def test_random_point_in_disk():
    assert all(
        math.sqrt(h ** 2 + v ** 2) <= 10
        for h, v in (random_point_in_disk(10) for _ in range(1000))
    )
