from ps2_analysis.fire_groups.recoil import Recoil


def test_half_horizontal_tolerance():
    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=2.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.half_horizontal_tolerance == 1.0

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=None,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.half_horizontal_tolerance is None


def test_max_tolerated_horizontal_kicks():
    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=1.0,
        horizontal_tolerance=1.8,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.max_tolerated_horizontal_kicks == 1

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=1.0,
        horizontal_tolerance=2.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.max_tolerated_horizontal_kicks == 2

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=1.0,
        horizontal_tolerance=None,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.max_tolerated_horizontal_kicks == -1


def test_max_horizontal_deviation():
    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=1.0,
        horizontal_tolerance=2.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.max_horizontal_deviation == 4.0

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=1.0,
        horizontal_tolerance=None,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.max_horizontal_deviation == -1


def test_angle_delta():
    recoil: Recoil = Recoil(
        max_angle=10.0,
        min_angle=7.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=4.0,
        min_horizontal=1.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.horizontal_delta == 3.0

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.angle_delta == 0.0


def test_horizontal_delta():
    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=4.0,
        min_horizontal=1.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.horizontal_delta == 3.0

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=4.0,
        min_horizontal=4.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.horizontal_delta == 0.0


def test_vertical_delta():
    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=4.0,
        min_vertical=1.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.vertical_delta == 3.0

    recoil: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=4.0,
        min_vertical=4.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    assert recoil.vertical_delta == 0.0
