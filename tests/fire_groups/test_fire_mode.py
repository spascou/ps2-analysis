from ps2_census.enums import FireModeType, PlayerState, ResistType

from ps2_analysis.enums import DamageTargetType
from ps2_analysis.fire_groups.ammo import Ammo
from ps2_analysis.fire_groups.cone_of_fire import ConeOfFire
from ps2_analysis.fire_groups.damage_profile import DamageProfile
from ps2_analysis.fire_groups.fire_mode import FireMode
from ps2_analysis.fire_groups.fire_timing import FireTiming
from ps2_analysis.fire_groups.recoil import Recoil


def test_damage_per_pellet():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
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
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.damage_per_pellet(0) == 90
    assert (
        fm.damage_per_pellet(0, damage_target_type=DamageTargetType.INFANTRY_NANOWEAVE)
        == 72
    )
    assert fm.damage_per_pellet(10) == 90
    assert fm.damage_per_pellet(15) == 50
    assert fm.damage_per_pellet(20) == 10
    assert fm.damage_per_pellet(30) == 10

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    fm.indirect_damage_profile = DamageProfile(
        max_damage=10,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.damage_per_pellet(0) == 100
    assert fm.damage_per_pellet(10) == 100
    assert fm.damage_per_pellet(15) == 60
    assert fm.damage_per_pellet(20) == 20
    assert fm.damage_per_pellet(30) == 20


def test_damage_per_shot():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
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
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.damage_per_shot(0) == 1500
    assert (
        fm.damage_per_shot(0, damage_target_type=DamageTargetType.INFANTRY_NANOWEAVE)
        == 1200
    )
    assert fm.damage_per_shot(100) == 1500
    assert fm.damage_per_shot(150) == 1000
    assert fm.damage_per_shot(200) == 500
    assert fm.damage_per_shot(300) == 500

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    fm.indirect_damage_profile = DamageProfile(
        max_damage=50,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=2,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.damage_per_shot(0) == 1550
    assert fm.damage_per_shot(100) == 1550
    assert fm.damage_per_shot(150) == 1050
    assert fm.damage_per_shot(200) == 550
    assert fm.damage_per_shot(300) == 550


def test_shots_to_kill():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
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
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=200,
        min_damage=500,
        min_damage_range=400,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.shots_to_kill(0) == 1
    assert fm.shots_to_kill(200) == 1
    assert fm.shots_to_kill(300.1) == 2
    assert fm.shots_to_kill(400) == 2
    assert fm.shots_to_kill(500) == 2

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=200,
        min_damage=500,
        min_damage_range=400,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    fm.indirect_damage_profile = DamageProfile(
        max_damage=100,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert fm.shots_to_kill(0) == 1
    assert fm.shots_to_kill(200) == 1
    assert fm.shots_to_kill(350.1) == 2
    assert fm.shots_to_kill(400) == 2
    assert fm.shots_to_kill(500) == 2


def test_shots_to_kill_ranges():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
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
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert list(fm.shots_to_kill_ranges()) == [(0.0, 1), (150.0, 2)]

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=ft,
        recoil=rc,
    )

    fm.direct_damage_profile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    fm.indirect_damage_profile = DamageProfile(
        max_damage=100,
        max_damage_range=1,
        min_damage=0,
        min_damage_range=3,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    assert list(fm.shots_to_kill_ranges()) == [(0.0, 1), (160.0, 2)]


def test_generate_real_shot_timings():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=100, fire_duration=0, delay=0, charge_up_time=0,
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

    am: Ammo = Ammo(
        clip_size=5,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=500,
        reload_chamber_time=500,
    )

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        ammo=am,
        fire_timing=ft,
        recoil=rc,
    )

    assert list(fm.generate_real_shot_timings(shots=7)) == [
        (0, True),
        (100, False),
        (200, False),
        (300, False),
        (400, False),
        (1400, True),
        (1500, False),
    ]

    assert list(fm.generate_real_shot_timings(shots=7, control_time=100)) == [
        (0, True),
        (100, False),
        (200, False),
        (300, False),
        (400, False),
        (1400, True),
        (1500, False),
    ]

    assert list(
        fm.generate_real_shot_timings(shots=7, control_time=100, auto_burst_length=2)
    ) == [
        (0, True),
        (100, False),
        (300, True),
        (400, False),
        (600, True),
        (1600, True),
        (1700, False),
    ]


def test_simulate_shots():
    ft: FireTiming = FireTiming(
        is_automatic=True, refire_time=100, fire_duration=0, delay=0, charge_up_time=0,
    )

    rc: Recoil = Recoil(
        max_angle=5.0,
        min_angle=10.0,
        max_vertical=1.0,
        min_vertical=3.0,
        vertical_increase=0.0,
        vertical_crouched_increase=0.0,
        max_horizontal=1.0,
        min_horizontal=2.0,
        horizontal_tolerance=0.0,
        max_horizontal_increase=0.0,
        min_horizontal_increase=0.0,
        recovery_acceleration=0.0,
        recovery_delay=0.0,
        recovery_rate=0.0,
        first_shot_multiplier=1.0,
    )

    am: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=1750,
        reload_chamber_time=0,
    )

    ddp: DamageProfile = DamageProfile(
        max_damage=1500,
        max_damage_range=100,
        min_damage=500,
        min_damage_range=200,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    cof: ConeOfFire = ConeOfFire(
        max_angle=1.0,
        min_angle=0.0,
        bloom=0.1,
        recovery_rate=20,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=1.5,
        pellet_spread=0.0,
    )

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=ddp,
        zoom=1.5,
        ammo=am,
        fire_timing=ft,
        recoil=rc,
        player_state_cone_of_fire={PlayerState.STANDING: cof},
    )

    assert [
        s[1][1] for s in fm.simulate_shots(shots=10, player_state=PlayerState.STANDING,)
    ] != [0.0] * 10

    assert [
        s[1][0]
        for s in fm.simulate_shots(
            shots=10, player_state=PlayerState.STANDING, recoil_compensation=True,
        )
    ] != [0.0] * 10

    assert [
        s[1][1]
        for s in fm.simulate_shots(
            shots=10, player_state=PlayerState.STANDING, recoil_compensation=True,
        )
    ] == [0.0] * 10


def test_real_time_to_kill():
    ft: FireTiming = FireTiming(
        is_automatic=True,
        refire_time=100,
        fire_duration=0,
        delay=0,
        charge_up_time=0,
        chamber_time=0,
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

    am: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=700,
        reload_chamber_time=300,
    )

    ddp: DamageProfile = DamageProfile(
        max_damage=1000,
        max_damage_range=10,
        min_damage=0,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    cof: ConeOfFire = ConeOfFire(
        max_angle=0.0,
        min_angle=0.0,
        bloom=0.0,
        recovery_rate=20,
        recovery_delay=100,
        multiplier=1.0,
        moving_multiplier=1.5,
        pellet_spread=0.0,
    )

    fm: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        direct_damage_profile=ddp,
        zoom=1.5,
        ammo=am,
        fire_timing=ft,
        recoil=rc,
        player_state_cone_of_fire={PlayerState.STANDING: cof},
    )

    assert fm.real_time_to_kill(distance=1.0, runs=10) == 0

    assert fm.real_time_to_kill(distance=10.0, runs=10) == 0

    assert fm.real_time_to_kill(distance=11.0, runs=10) == 100

    assert fm.real_time_to_kill(distance=15.0, runs=10) == 100

    assert fm.real_time_to_kill(distance=16.0, runs=10) == 200

    assert fm.real_time_to_kill(distance=20.0, runs=10) == -1
