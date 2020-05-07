from ps2_analysis.infantry_weapons.damage_profile import DamageLocation, DamageProfile


def test_damage_delta():
    dp: DamageProfile = DamageProfile(
        max_damage=100,
        max_damage_range=1234,
        min_damage=100,
        min_damage_range=5678,
        pellets_count=1,
    )
    assert dp.damage_delta == 0

    dp: DamageProfile = DamageProfile(
        max_damage=100,
        max_damage_range=1234,
        min_damage=90,
        min_damage_range=5678,
        pellets_count=1,
    )
    assert dp.damage_delta == 10


def test_damage_range_delta():
    dp: DamageProfile = DamageProfile(
        max_damage=5678,
        max_damage_range=0,
        min_damage=1234,
        min_damage_range=0,
        pellets_count=1,
    )
    assert dp.damage_range_delta == 0

    dp: DamageProfile = DamageProfile(
        max_damage=5678,
        max_damage_range=10,
        min_damage=1234,
        min_damage_range=100,
        pellets_count=1,
    )
    assert dp.damage_range_delta == 90


def test_damage_per_pellet():
    dp: DamageProfile = DamageProfile(
        max_damage=100,
        max_damage_range=0,
        min_damage=100,
        min_damage_range=0,
        pellets_count=1,
    )
    assert dp.damage_per_pellet(0) == 100
    assert dp.damage_per_pellet(10) == 100
    assert dp.damage_per_pellet(1000) == 100

    dp: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
    )
    assert dp.damage_per_pellet(0) == 90
    assert dp.damage_per_pellet(10) == 90
    assert dp.damage_per_pellet(15) == 50
    assert dp.damage_per_pellet(20) == 10
    assert dp.damage_per_pellet(30) == 10


def test_damage_per_shot():
    dp: DamageProfile = DamageProfile(
        max_damage=100,
        max_damage_range=0,
        min_damage=100,
        min_damage_range=0,
        pellets_count=4,
    )

    assert dp.damage_per_shot(0) == 4 * dp.damage_per_pellet(0)


def test_damage_location():
    dp: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        location_multiplier={DamageLocation.HEAD: 2.0},
        pellets_count=1,
    )

    assert dp.damage_per_pellet(0, location=DamageLocation.HEAD) == 180
    assert dp.damage_per_pellet(10, location=DamageLocation.HEAD) == 180
    assert dp.damage_per_pellet(15, location=DamageLocation.HEAD) == 100
    assert dp.damage_per_pellet(20, location=DamageLocation.HEAD) == 20
    assert dp.damage_per_pellet(30, location=DamageLocation.HEAD) == 20

    assert dp.damage_per_pellet(0, location=DamageLocation.LEGS) == 90
    assert dp.damage_per_pellet(10, location=DamageLocation.LEGS) == 90
    assert dp.damage_per_pellet(15, location=DamageLocation.LEGS) == 50
    assert dp.damage_per_pellet(20, location=DamageLocation.LEGS) == 10
    assert dp.damage_per_pellet(30, location=DamageLocation.LEGS) == 10


def test_shots_to_kill():
    dp: DamageProfile = DamageProfile(
        max_damage=500,
        max_damage_range=10,
        min_damage=100,
        min_damage_range=20,
        location_multiplier={DamageLocation.HEAD: 2.0},
        pellets_count=1,
    )

    assert dp.shots_to_kill(0) == 2
    assert dp.shots_to_kill(0, location=DamageLocation.HEAD) == 1

    assert dp.shots_to_kill(30) == 10
    assert dp.shots_to_kill(30, location=DamageLocation.HEAD) == 5
