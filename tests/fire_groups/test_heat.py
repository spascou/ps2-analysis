from ps2_analysis.fire_groups.heat import Heat


def test_shots_before_overheat():
    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_before_overheat == -1

    heat: Heat = Heat(
        total_capacity=0,
        heat_per_shot=100,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_before_overheat == 0

    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=90,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_before_overheat == 11

    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=100,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_before_overheat == 10


def test_shots_to_overheat():
    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=90,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_to_overheat == 12

    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=100,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    assert heat.shots_to_overheat == 11


def test_recovery_time():
    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=5,
        recovery_rate=100_000,
    )

    assert heat.recovery_time(1000) == 15
    assert heat.recovery_time(500) == 10

    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=5,
        recovery_rate=90_000,
    )

    assert heat.recovery_time(1000) == 17


def test_full_recovery_time():
    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=5,
        recovery_rate=100_000,
    )

    assert heat.full_recovery_time == heat.recovery_time(1000)


def test_overheat_recovery_time():
    heat: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=15,
        recovery_delay=5,
        recovery_rate=100_000,
    )

    assert heat.overheat_recovery_time == 15 + heat.full_recovery_time
