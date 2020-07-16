from typing import Dict

from ps2_census.enums import FireModeType, PlayerState, ProjectileFlightType, ResistType

from ps2_analysis.fire_groups.ammo import Ammo
from ps2_analysis.fire_groups.cone_of_fire import ConeOfFire
from ps2_analysis.fire_groups.damage_profile import DamageProfile
from ps2_analysis.fire_groups.fire_group import FireGroup
from ps2_analysis.fire_groups.fire_mode import FireMode
from ps2_analysis.fire_groups.fire_timing import FireTiming
from ps2_analysis.fire_groups.heat import Heat
from ps2_analysis.fire_groups.lock_on import LockOn
from ps2_analysis.fire_groups.projectile import Projectile
from ps2_analysis.fire_groups.recoil import Recoil


def test_fire_modes_attributes():
    # Fire timing
    fit_1: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
    )
    fit_2: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
    )

    # Recoil
    rec_1: Recoil = Recoil(
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
    rec_2: Recoil = Recoil(
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

    # Player state cone of fire
    psc_1: Dict[PlayerState, ConeOfFire] = {
        PlayerState.STANDING: ConeOfFire(
            max_angle=2.0,
            min_angle=1.0,
            bloom=0.1,
            recovery_rate=10.0,
            recovery_delay=100,
            multiplier=2.0,
            moving_multiplier=2.0,
            pellet_spread=0.0,
        )
    }
    psc_2: Dict[PlayerState, ConeOfFire] = {
        PlayerState.STANDING: ConeOfFire(
            max_angle=2.0,
            min_angle=1.0,
            bloom=0.1,
            recovery_rate=10.0,
            recovery_delay=100,
            multiplier=2.0,
            moving_multiplier=2.0,
            pellet_spread=0.0,
        )
    }

    # Player state can ADS
    psa_1: Dict[PlayerState, bool] = {PlayerState.STANDING: True}
    psa_2: Dict[PlayerState, bool] = {PlayerState.STANDING: True}

    # Projectile
    prj_1: Projectile = Projectile(
        speed=100,
        gravity=0.0,
        life_time=3000,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )
    prj_2: Projectile = Projectile(
        speed=100,
        gravity=0.0,
        life_time=3000,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )

    # Lock-on
    lon_1: LockOn = LockOn(
        life_time=100, seek_in_flight=False, maintain=False, required=True,
    )
    lon_2: LockOn = LockOn(
        life_time=100, seek_in_flight=False, maintain=False, required=True,
    )

    # Damage profile
    ddp_1: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    ddp_2: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    # Indirect damage profile
    idp_1: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=1,
        min_damage=20,
        min_damage_range=2,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )
    idp_2: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=1,
        min_damage=20,
        min_damage_range=2,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    # Ammo
    amm_1: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=0,
        reload_chamber_time=0,
    )
    amm_2: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=0,
        reload_chamber_time=0,
    )

    # Heat
    hea_1: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )
    hea_2: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    # Fire modes
    fm_1: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=fit_1,
        recoil=rec_1,
        player_state_cone_of_fire=psc_1,
        player_state_can_ads=psa_1,
        projectile=prj_1,
        lock_on=lon_1,
        direct_damage_profile=ddp_1,
        indirect_damage_profile=idp_1,
        ammo=amm_1,
        heat=hea_1,
    )
    fm_2: FireMode = FireMode(
        fire_mode_id=1,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=fit_2,
        recoil=rec_2,
        player_state_cone_of_fire=psc_2,
        player_state_can_ads=psa_2,
        projectile=prj_2,
        lock_on=lon_2,
        direct_damage_profile=ddp_2,
        indirect_damage_profile=idp_2,
        ammo=amm_2,
        heat=hea_2,
    )

    # Fire group
    fg: FireGroup = FireGroup(
        fire_group_id=2, description="", transition_time=0, fire_modes=[fm_1, fm_2]
    )
    assert fg.fire_timing == fm_1.fire_timing
    assert fg.recoil == fm_1.recoil
    assert fg.player_state_cone_of_fire == fm_1.player_state_cone_of_fire
    assert fg.player_state_can_ads == fm_1.player_state_can_ads
    assert fg.projectile == fm_1.projectile
    assert fg.lock_on == fm_1.lock_on
    assert fg.direct_damage_profile == fm_1.direct_damage_profile
    assert fg.indirect_damage_profile == fm_1.indirect_damage_profile
    assert fg.ammo == fm_1.ammo
    assert fg.heat == fm_1.heat


def test_no_fire_modes_attributes():
    # Fire timing
    fit_1: FireTiming = FireTiming(
        is_automatic=True, refire_time=0, fire_duration=0, delay=0, charge_up_time=0,
    )
    fit_2: FireTiming = FireTiming(
        is_automatic=True, refire_time=100, fire_duration=0, delay=0, charge_up_time=0,
    )

    # Recoil
    rec_1: Recoil = Recoil(
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
    rec_2: Recoil = Recoil(
        max_angle=1.0,
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

    # Player state cone of fire
    psc_1: Dict[PlayerState, ConeOfFire] = {
        PlayerState.STANDING: ConeOfFire(
            max_angle=1.0,
            min_angle=1.0,
            bloom=0.1,
            recovery_rate=10.0,
            recovery_delay=100,
            multiplier=2.0,
            moving_multiplier=2.0,
            pellet_spread=0.0,
        )
    }
    psc_2: Dict[PlayerState, ConeOfFire] = {
        PlayerState.STANDING: ConeOfFire(
            max_angle=2.0,
            min_angle=1.0,
            bloom=0.1,
            recovery_rate=10.0,
            recovery_delay=100,
            multiplier=2.0,
            moving_multiplier=2.0,
            pellet_spread=0.0,
        )
    }

    # Player state can ADS
    psa_1: Dict[PlayerState, bool] = {PlayerState.STANDING: True}
    psa_2: Dict[PlayerState, bool] = {PlayerState.STANDING: False}

    # Projectile
    prj_1: Projectile = Projectile(
        speed=100,
        gravity=0.0,
        life_time=3000,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )
    prj_2: Projectile = Projectile(
        speed=200,
        gravity=0.0,
        life_time=3000,
        flight_type=ProjectileFlightType.BALLISTIC,
        drag=0.0,
    )

    # Lock-on
    lon_1: LockOn = LockOn(
        life_time=100, seek_in_flight=False, maintain=False, required=True,
    )
    lon_2: LockOn = LockOn(
        life_time=200, seek_in_flight=False, maintain=False, required=True,
    )

    # Damage profile
    ddp_1: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    ddp_2: DamageProfile = DamageProfile(
        max_damage=95,
        max_damage_range=10,
        min_damage=10,
        min_damage_range=20,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    # Indirect damage profile
    idp_1: DamageProfile = DamageProfile(
        max_damage=92,
        max_damage_range=1,
        min_damage=20,
        min_damage_range=2,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )
    idp_2: DamageProfile = DamageProfile(
        max_damage=90,
        max_damage_range=1,
        min_damage=20,
        min_damage_range=2,
        pellets_count=1,
        resist_type=ResistType.SMALL_ARM,
    )

    # Ammo
    amm_1: Ammo = Ammo(
        clip_size=12,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=0,
        reload_chamber_time=0,
    )
    amm_2: Ammo = Ammo(
        clip_size=10,
        total_capacity=100,
        ammo_per_shot=1,
        short_reload_time=0,
        reload_chamber_time=0,
    )

    # Heat
    hea_1: Heat = Heat(
        total_capacity=1000,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )
    hea_2: Heat = Heat(
        total_capacity=1200,
        heat_per_shot=0,
        overheat_penalty_time=0,
        recovery_delay=0,
        recovery_rate=0,
    )

    # Fire modes
    fm_1: FireMode = FireMode(
        fire_mode_id=0,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=fit_1,
        recoil=rec_1,
        player_state_cone_of_fire=psc_1,
        player_state_can_ads=psa_1,
        projectile=prj_1,
        lock_on=lon_1,
        direct_damage_profile=ddp_1,
        indirect_damage_profile=idp_1,
        ammo=amm_1,
        heat=hea_1,
    )
    fm_2: FireMode = FireMode(
        fire_mode_id=1,
        fire_mode_type=FireModeType.IRON_SIGHT,
        description="",
        is_ads=True,
        detect_range=30.0,
        move_multiplier=1.0,
        turn_multiplier=1.0,
        zoom=1.5,
        fire_timing=fit_2,
        recoil=rec_2,
        player_state_cone_of_fire=psc_2,
        player_state_can_ads=psa_2,
        projectile=prj_2,
        lock_on=lon_2,
        direct_damage_profile=ddp_2,
        indirect_damage_profile=idp_2,
        ammo=amm_2,
        heat=hea_2,
    )

    # Fire group
    fg: FireGroup = FireGroup(
        fire_group_id=2, description="", transition_time=0, fire_modes=[fm_1, fm_2]
    )
    assert fg.fire_timing is None
    assert fg.recoil is None
    assert fg.player_state_cone_of_fire is None
    assert fg.player_state_can_ads is None
    assert fg.projectile is None
    assert fg.lock_on is None
    assert fg.direct_damage_profile is None
    assert fg.indirect_damage_profile is None
    assert fg.ammo is None
    assert fg.heat is None
