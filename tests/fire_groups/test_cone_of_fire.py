from ps2_analysis.fire_groups.cone_of_fire import ConeOfFire


def test_min_cof_angle():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=2.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.min_cof_angle(moving=False) == 2.0
    assert cof.min_cof_angle(moving=True) == 4.0


def test_max_cof_angle():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=2.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.max_cof_angle(moving=False) == 4.0
    assert cof.max_cof_angle(moving=True) == 8.0


def test_apply_bloom():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=2.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.apply_bloom(current=1.0, moving=False) == 1.1
    assert cof.apply_bloom(current=2.0, moving=False) == 2.1
    assert cof.apply_bloom(current=3.9, moving=False) == 4.0
    assert cof.apply_bloom(current=4.0, moving=False) == 4.0
    assert cof.apply_bloom(current=4.1, moving=False) == 4.0


def test_recover():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=1.0,
        pellet_spread=0.0,
    )

    assert cof.recover(current=2.0, time=10) == 1.9
    assert cof.recover(current=2.0, time=50) == 1.5
    assert cof.recover(current=2.0, time=100) == 1.0
    assert cof.recover(current=2.0, time=200) == 1.0
    assert cof.recover(current=2.0, time=300) == 1.0

    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=0.0,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=1.0,
        pellet_spread=0.0,
    )

    assert cof.recover(current=2.0, time=1000) == 2.0


def test_recover_time():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.recover_time(current=2.0) == 200

    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=0.0,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.recover_time(current=2.0) == -1


def test_max_recover_time():
    cof: ConeOfFire = ConeOfFire(
        max_angle=2.0,
        min_angle=1.0,
        bloom=0.1,
        recovery_rate=10.0,
        recovery_delay=100,
        multiplier=2.0,
        moving_multiplier=2.0,
        pellet_spread=0.0,
    )

    assert cof.max_recover_time(moving=False) == 400
    assert cof.max_recover_time(moving=True) == 800
