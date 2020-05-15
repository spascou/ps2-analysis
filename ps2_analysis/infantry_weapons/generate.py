import json
from typing import Dict, FrozenSet, List, Optional

from ps2_census.enums import (
    Faction,
    FireModeType,
    ItemCategory,
    PlayerState,
    ProjectileFlightType,
)
from slugify import slugify

from ps2_analysis.data_file import DataFile, load_data_file
from ps2_analysis.utils import get, optget

from .ammo import Ammo
from .attachment import Attachment
from .cone_of_fire import ConeOfFire
from .damage_profile import DamageLocation, DamageProfile
from .data_fixers import INFANTRY_WEAPONS_DATA_FIXERS
from .fire_group import FireGroup
from .fire_mode import FireMode
from .fire_timing import FireTiming
from .heat import Heat
from .infantry_weapon import InfantryWeapon
from .projectile import Projectile
from .recoil import Recoil

EXCLUDED_ITEM_IDS: FrozenSet[int] = frozenset(
    (6008686, 6004198,)  # Grenade printer  # Mystery Weapon
)


def generate_infantry_weapons(data_files_directory: str) -> List[InfantryWeapon]:
    print("Generating infantry weapon objects")

    raw: List[dict] = load_data_file(
        data_file=DataFile.INFANTRY_WEAPONS, directory=data_files_directory
    )

    filtered: List[dict] = filter_infantry_weapons(raw)

    weapons: List[InfantryWeapon] = parse_infantry_weapons_data(filtered)
    print(f"Generated {len(weapons)} infantry weapon objects")

    return weapons


def filter_infantry_weapons(data: List[dict]) -> List[dict]:
    ifw: List[dict] = list(
        filter(lambda x: (int(x["item_id"]) not in EXCLUDED_ITEM_IDS), data)
    )

    return ifw


def parse_infantry_weapons_data(data: List[dict]) -> List[InfantryWeapon]:
    infantry_weapons: List[InfantryWeapon] = []

    d: dict
    for d in data:
        item_id: int = get(d, "item_id", int)

        if item_id in INFANTRY_WEAPONS_DATA_FIXERS:
            INFANTRY_WEAPONS_DATA_FIXERS[item_id](d)

        try:
            w: dict = d["item_to_weapon"]["weapon"]
            w_d: Optional[dict] = d.get("weapon_datasheet")

            if w_d is None:
                print(f"{d['name']['en']} ({d['item_id']}) IS FUCKED")
                continue

            # Infantry weapons
            infantry_weapon: InfantryWeapon = InfantryWeapon(
                # Basic information
                item_id=item_id,
                weapon_id=get(w, "weapon_id", int),
                name=d["name"]["en"],
                description=d["description"]["en"],
                slug=slugify(d["name"]["en"]),
                image_path=d.get("image_path"),
                faction=Faction(optget(d, "faction_id", int, 0)),
                category=ItemCategory(get(d, "item_category_id", int)),
                # Movement modifiers
                move_multiplier=get(w, "move_modifier", float),
                turn_multiplier=get(w, "turn_modifier", float),
                # Handling timings
                equip_time=get(w, "equip_ms", int),
                unequip_time=get(w, "unequip_ms", int),
                from_ads_time=get(w, "from_iron_sights_ms", int),
                to_ads_time=get(w, "to_iron_sights_ms", int),
                sprint_recovery_time=get(w, "sprint_recovery_ms", int),
            )

            # Fire groups
            _fg: dict
            for _fg in sorted(
                w["weapon_to_fire_groups"],
                key=lambda x: optget(x, "fire_group_index", int, 0),
            ):
                fg: dict = _fg["fire_group"]

                fire_group: FireGroup = FireGroup(
                    # General information
                    index=optget(fg, "fire_group_index", int, 0),
                    transition_time=optget(fg, "transition_duration_ms", int, 0),
                )

                _fm: dict
                for _fm in sorted(
                    fg["fire_group_to_fire_modes"],
                    key=lambda x: get(x, "fire_mode_id", int),
                ):
                    fm: dict = _fm["fire_mode"]
                    pr: dict = fm["fire_mode_to_projectile"]["projectile"]

                    # Player states
                    player_state_cone_of_fire: Dict[PlayerState, ConeOfFire] = {}
                    player_state_can_ads: Dict[PlayerState, bool] = {}

                    ps: dict
                    for ps in sorted(
                        fm["player_state_groups"],
                        key=lambda x: get(x, "player_state_id", int),
                    ):
                        player_state_cone_of_fire[
                            PlayerState(get(ps, "player_state_id", int))
                        ] = ConeOfFire(
                            # Basic information
                            max_angle=get(ps, "cof_max", float),
                            min_angle=get(ps, "cof_min", float),
                            bloom=get(fm, "cof_recoil", float),
                            # Recovery
                            recovery_rate=get(ps, "cof_recovery_rate", float),
                            recovery_delay=get(ps, "cof_recovery_delay_ms", int),
                            recovery_delay_threshold=get(
                                ps, "cof_recovery_delay_threshold", int
                            ),
                            # Multipliers
                            multiplier=get(fm, "cof_scalar", float),
                            moving_multiplier=get(fm, "cof_scalar", float),
                            # Pellet
                            pellet_spread=optget(fm, "cof_pellet_spread", float),
                            # Misc
                            grow_rate=get(ps, "cof_grow_rate", float),
                            shots_before_penalty=get(
                                ps, "cof_shots_before_penalty", int
                            ),
                            turn_penalty=get(ps, "cof_turn_penalty", float),
                            range=get(fm, "cof_range", float),
                        )

                        player_state_can_ads[
                            PlayerState(get(ps, "player_state_id", int))
                        ] = (get(ps, "can_iron_sight", int) == 1)

                    fire_mode: FireMode = FireMode(
                        # Basic information
                        type=FireModeType(get(fm, "fire_mode_type_id", int)),
                        description=fm["description"]["en"],
                        is_ads=optget(fm, "iron_sights", lambda x: int(x) == 1, False),
                        detect_range=optget(fm, "fire_detect_range", int, 0),
                        # Movement modifiers
                        turn_multiplier=get(fm, "turn_modifier", float),
                        move_multiplier=get(fm, "move_modifier", float),
                        # Damage profiles
                        direct_damage_profile=DamageProfile(
                            # Base damage
                            max_damage=get(fm, "max_damage", int),
                            max_damage_range=optget(fm, "max_damage_range", int, 0),
                            min_damage=optget(
                                fm, "min_damage", int, get(fm, "max_damage", int)
                            ),
                            min_damage_range=get(fm, "min_damage_range", int),
                            # Pellets
                            pellets_count=get(fm, "fire_pellets_per_shot", int),
                            # Locational modifiers
                            location_multiplier={
                                DamageLocation.HEAD: 1.0
                                + optget(fm, "damage_head_multiplier", float, 0.0),
                                DamageLocation.LEGS: 1.0
                                + optget(fm, "damage_legs_multiplier", float, 0.0),
                            },
                        ),
                        indirect_damage_profile=(
                            DamageProfile(
                                # Base damage
                                max_damage=int(fm["max_damage_ind"]),
                                max_damage_range=int(fm["max_damage_ind_radius"]),
                                min_damage=int(fm["min_damage_ind"]),
                                min_damage_range=int(fm["min_damage_ind_radius"]),
                                pellets_count=1,
                            )
                            if "max_indirect_damage" in fm
                            else None
                        ),
                        # Zoom
                        zoom=get(fm, "zoom_default", float),
                        # Sway
                        sway_can_steady=optget(
                            fm, "sway_can_steady", lambda x: int(x) == 1
                        ),
                        sway_amplitude_x=optget(fm, "sway_amplitude_x", float),
                        sway_amplitude_y=optget(fm, "sway_amplitude_y", float),
                        sway_period_x=optget(fm, "sway_period_x", float),
                        sway_period_y=optget(fm, "sway_period_y", float),
                        # Ammo
                        ammo=(
                            Ammo(
                                # Basic information
                                clip_size=get(w_d, "clip_size", int),
                                total_capacity=get(w_d, "capacity", int),
                                ammo_per_shot=get(fm, "fire_ammo_per_shot", int),
                                block_auto=optget(
                                    fm, "reload_block_auto", lambda x: int(x) == 1
                                ),
                                continuous=optget(
                                    fm, "reload_continuous", lambda x: int(x) == 1
                                ),
                                # Reload
                                short_reload_time=get(fm, "reload_time_ms", int),
                                reload_chamber_time=optget(
                                    fm, "reload_chamber_ms", int, 0
                                ),
                                loop_start_time=optget(fm, "reload_loop_start_ms", int),
                                loop_end_time=optget(fm, "reload_loop_end_ms", int),
                                # Chamber
                                can_chamber_in_ads=optget(
                                    fg,
                                    "can_chamber_ironsights",
                                    lambda x: int(x) == 1,
                                    None,
                                ),
                            )
                            if optget(w_d, "capacity", int, 0) > 0
                            else None
                        ),
                        heat=(
                            Heat(
                                # Basic information
                                total_capacity=get(w, "heat_capacity", int),
                                heat_per_shot=get(fm, "heat_per_shot", int),
                                # Heat management
                                overheat_penalty_time=optget(
                                    w, "heat_overheat_penalty_ms", int, 0
                                ),
                                recovery_delay=optget(
                                    fm, "heat_recovery_delay_ms", int, 0
                                ),
                                recovery_rate=get(w, "heat_bleed_off_rate", int),
                                threshold=get(fm, "heat_threshold", int),
                            )
                            if optget(w, "heat_capacity", int, 0) > 0
                            else None
                        ),
                        # Fire timing
                        fire_timing=FireTiming(
                            # Basic information
                            is_automatic=optget(
                                fm, "is_automatic", lambda x: int(x) == 1, False
                            ),
                            refire_time=get(fm, "fire_refire_ms", int),
                            fire_duration=optget(fm, "fire_duration_ms", int),
                            # Burst
                            burst_length=optget(fm, "fire_burst_count", int),
                            burst_refire_time=optget(fm, "fire_auto_fire_ms", int),
                            # Delay
                            delay=optget(fm, "fire_delay_ms", int, 0),
                            # Charge
                            charge_up_time=optget(fm, "fire_charge_up_ms", int, 0),
                            # Spooling
                            spool_up_time=optget(fg, "spool_up_ms", int),
                            spool_up_initial_refire_time=optget(
                                fg, "spool_up_initial_refire_ms", int
                            ),
                            # Chambering
                            chamber_time=optget(fg, "chamber_duration_ms", int),
                        ),
                        # Recoil
                        recoil=Recoil(
                            # Angle
                            max_angle=optget(fm, "recoil_angle_max", float, 0.0),
                            min_angle=optget(fm, "recoil_angle_min", float, 0.0),
                            # Vertical
                            max_vertical=get(fm, "recoil_magnitude_max", float),
                            min_vertical=get(fm, "recoil_magnitude_min", float),
                            vertical_increase=optget(fm, "recoil_increase", float, 0.0),
                            vertical_crouched_increase=optget(
                                fm, "recoil_increase_crouched", float, 0.0
                            ),
                            # Horizontal
                            max_horizontal=get(fm, "recoil_horizontal_max", float),
                            min_horizontal=get(fm, "recoil_horizontal_min", float),
                            horizontal_tolerance=optget(
                                fm, "recoil_horizontal_tolerance", float
                            ),
                            max_horizontal_increase=optget(
                                fm, "recoil_horizontal_max_increase", float, 0.0
                            ),
                            min_horizontal_increase=optget(
                                fm, "recoil_horizontal_min_increase", float, 0.0
                            ),
                            # Recovery
                            recovery_acceleration=get(
                                fm, "recoil_recovery_acceleration", float
                            ),
                            recovery_delay=optget(
                                fm, "recoil_recovery_delay_ms", int, 0
                            ),
                            recovery_rate=get(fm, "recoil_recovery_rate", float),
                            # Misc
                            first_shot_multiplier=get(
                                fm, "recoil_first_shot_modifier", float
                            ),
                            shots_at_min_magnitude=optget(
                                fm, "recoil_shots_at_min_magnitude", int
                            ),
                            max_total_magnitude=optget(
                                fm, "recoil_max_total_magnitude", float
                            ),
                        ),
                        # Projectile
                        projectile=Projectile(
                            # Speed
                            speed=optget(fm, "projectile_speed_override", float)
                            or get(pr, "speed", float),
                            max_speed=optget(pr, "speed_max", float),
                            acceleration=optget(pr, "acceleration", float),
                            # Trajectory
                            flight_type=ProjectileFlightType(
                                get(pr, "projectile_flight_type_id", int)
                            ),
                            gravity=optget(pr, "gravity", float),
                            turn_rate=optget(pr, "turn_rate", float),
                            # Misc
                            life_time=get(
                                pr, "lifespan", lambda x: int(1_000 * float(x))
                            ),
                            drag=optget(pr, "drag", float),
                        ),
                        # Player state cone of fire
                        player_state_cone_of_fire=player_state_cone_of_fire,
                        # Player state can ads
                        player_state_can_ads=player_state_can_ads,
                    )

                    fire_group.fire_modes.append(fire_mode)

                infantry_weapon.fire_groups.append(fire_group)

            infantry_weapons.append(infantry_weapon)

            _at: dict
            for _at in sorted(
                d.get("item_attachments", []),
                key=lambda x: get(x, "attachment_item_id", int),
            ):
                at: dict = _at["item"]

                attachment: Attachment = Attachment(
                    item_id=get(at, "item_id", int),
                    name=at["name"]["en"],
                    description=at.get("description", {"en": None})["en"],
                    image_path=at.get("image_path"),
                    is_default=get(at, "is_default_attachment", int) == 1,
                )

                for zef in at.get("zone_effects", []):
                    p_zef: dict = {}

                    # Effect Type
                    eft: dict = zef["zone_effect_type"]

                    p_zef["action"] = eft["description"]

                    for k, v in eft.items():
                        if k.startswith("string") or k.startswith("param"):
                            if k in zef:
                                p_zef[eft[k]] = v

                    attachment.effects.append(p_zef)

                infantry_weapon.attachments.append(attachment)

        except (KeyError, ValueError, AssertionError) as e:
            print(json.dumps(d, sort_keys=True, indent=2))
            raise e

    return infantry_weapons