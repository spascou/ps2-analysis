from ps2_analysis.fire_groups.damage_profile import DamageLocation
from ps2_analysis.geometry_utils import determine_planetman_hit_location


def test_determine_planetman_hit_location():
    assert (
        determine_planetman_hit_location(x=0.0, y=0.0, aim_location=DamageLocation.HEAD)
        == DamageLocation.HEAD
    )
    assert (
        determine_planetman_hit_location(
            x=0.0, y=0.0, aim_location=DamageLocation.TORSO
        )
        == DamageLocation.TORSO
    )
    assert (
        determine_planetman_hit_location(x=0.0, y=0.0, aim_location=DamageLocation.LEGS)
        == DamageLocation.LEGS
    )
