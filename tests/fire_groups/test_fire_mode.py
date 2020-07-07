from ps2_census.enums import FireModeType

from ps2_analysis.fire_groups.damage_profile import DamageProfile
from ps2_analysis.fire_groups.fire_mode import FireMode
from ps2_analysis.fire_groups.fire_timing import FireTiming
from ps2_analysis.fire_groups.recoil import Recoil


def test_damage_per_pellet():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=0,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )

    rc: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_acceleration=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    fm: FireMode = FireMode(
        type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=None,
        indirect_damage_profile=None,
        zoom=1.5,
        sway_can_steady=None,
        sway_amplitude_x=None,
        sway_amplitude_y=None,
        sway_period_x=None,
        sway_period_y=None,
        ammo=None,
        heat=None,
        fire_timing=ft,
        recoil=rc,
        projectile=None,
        player_state_cone_of_fire={},
        player_state_can_ads={},
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
    )

    assert fm.damage_per_pellet(0) == 90
    assert fm.damage_per_pellet(10) == 90
    assert fm.damage_per_pellet(15) == 50
    assert fm.damage_per_pellet(20) == 10
    assert fm.damage_per_pellet(30) == 10

    fm.indirect_damage_profile = DamageProfile(
        max_damage=10,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
    )

    assert fm.damage_per_pellet(0) == 100
    assert fm.damage_per_pellet(10) == 100
    assert fm.damage_per_pellet(15) == 60
    assert fm.damage_per_pellet(20) == 20
    assert fm.damage_per_pellet(30) == 20


def test_damage_per_shot():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=0,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )

    rc: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_acceleration=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    fm: FireMode = FireMode(
        type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=None,
        indirect_damage_profile=None,
        zoom=1.5,
        sway_can_steady=None,
        sway_amplitude_x=None,
        sway_amplitude_y=None,
        sway_period_x=None,
        sway_period_y=None,
        ammo=None,
        heat=None,
        fire_timing=ft,
        recoil=rc,
        projectile=None,
        player_state_cone_of_fire={},
        player_state_can_ads={},
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
    )

    assert fm.damage_per_shot(0) == 1500
    assert fm.damage_per_shot(100) == 1500
    assert fm.damage_per_shot(150) == 1000
    assert fm.damage_per_shot(200) == 500
    assert fm.damage_per_shot(300) == 500

    fm.indirect_damage_profile = DamageProfile(
        max_damage=50,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=2,
        pellets_count=1,
    )

    assert fm.damage_per_shot(0) == 1550
    assert fm.damage_per_shot(100) == 1550
    assert fm.damage_per_shot(150) == 1050
    assert fm.damage_per_shot(200) == 550
    assert fm.damage_per_shot(300) == 550


def test_shots_to_kill():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=0,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )

    rc: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_acceleration=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    fm: FireMode = FireMode(
        type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=None,
        indirect_damage_profile=None,
        zoom=1.5,
        sway_can_steady=None,
        sway_amplitude_x=None,
        sway_amplitude_y=None,
        sway_period_x=None,
        sway_period_y=None,
        ammo=None,
        heat=None,
        fire_timing=ft,
        recoil=rc,
        projectile=None,
        player_state_cone_of_fire={},
        player_state_can_ads={},
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=200,
        min_damage=500,
        min_damage_range=400,
        pellets_count=1,
    )

    assert fm.shots_to_kill(0) == 1
    assert fm.shots_to_kill(200) == 1
    assert fm.shots_to_kill(300.1) == 2
    assert fm.shots_to_kill(400) == 2
    assert fm.shots_to_kill(500) == 2

    fm.indirect_damage_profile = DamageProfile(
        max_damage=100,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
    )

    assert fm.shots_to_kill(0) == 1
    assert fm.shots_to_kill(200) == 1
    assert fm.shots_to_kill(350.1) == 2
    assert fm.shots_to_kill(400) == 2
    assert fm.shots_to_kill(500) == 2


def test_shots_to_kill_ranges():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=0,
        fire_duration=None,
        burst_length=None,
        burst_refire_time=None,
        delay=0,
        charge_up_time=0,
        spool_up_time=None,
        spool_up_initial_refire_time=None,
        chamber_time=None,
    )

    rc: Recoil = Recoil(
        max_angle=0.0,
        min_angle=0.0,
        max_vertical=0.0,
        min_vertical=0.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=0.0,
        min_horizontal=0.0,
        horizontal_tolerance=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_acceleration=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    fm: FireMode = FireMode(
        type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=None,
        indirect_damage_profile=None,
        zoom=1.5,
        sway_can_steady=None,
        sway_amplitude_x=None,
        sway_amplitude_y=None,
        sway_period_x=None,
        sway_period_y=None,
        ammo=None,
        heat=None,
        fire_timing=ft,
        recoil=rc,
        projectile=None,
        player_state_cone_of_fire={},
        player_state_can_ads={},
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
    )

    assert fm.shots_to_kill_ranges() == [(0.0, 1), (150.0, 2)]

    fm.indirect_damage_profile = DamageProfile(
        max_damage=100,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
    )

    assert fm.shots_to_kill_ranges() == [(0.0, 1), (160.0, 2)]
