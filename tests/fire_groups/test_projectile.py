from ps2_census.enums import ProjectileFlightType

from ps2_analysis.fire_groups.projectile import Projectile


def test_max_range():
    projectile: Projectile = Projectile(
        speed=100,
        gravity=0.0,
        life_time=3000,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )

    assert projectile.max_range == 300

    projectile: Projectile = Projectile(
        speed=100,
        gravity=0.0,
        life_time=-1,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )

    assert projectile.max_range == -1
