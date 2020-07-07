from ps2_census.enums import ProjectileFlightType

from ps2_analysis.fire_groups.projectile import Projectile


def test_max_range():
    projectile: Projectile = Projectile(
        speed=100,
        max_speed=None,
        acceleration=None,
        flight_type=ProjectileFlightType.BALLISTIC,
        gravity=None,
        turn_rate=None,
        life_time=3000,
        drag=None,
    )

    assert projectile.max_range == 300
