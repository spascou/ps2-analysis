from typing import Dict, FrozenSet, List, Set, Tuple

from ps2_census.enums import Faction, ItemCategory
from slugify import slugify

from ps2_analysis.fire_groups.data_files import (
    load_data_files as load_fire_groups_data_files,
)
from ps2_analysis.fire_groups.fire_group import FireGroup
from ps2_analysis.fire_groups.generate import parse_fire_group_data
from ps2_analysis.utils import get, optget
from ps2_analysis.weapons.attachment import Attachment

from .data_files import load_data_files as load_vehicle_weapons_data_files
from .data_fixers import VEHICLE_WEAPONS_DATA_FIXERS
from .vehicle_weapon import VehicleWeapon

EXCLUDED_ITEM_IDS: FrozenSet[int] = frozenset(
    (
        728,
        729,
        731,
        732,
        6002396,
        6002397,
        6002398,
        6004400,
        6004444,
        6004445,
        6006068,
        6006069,
    )
)  # turrets


def generate_vehicle_weapons(data_files_directory: str) -> List[VehicleWeapon]:
    print("Generating vehicle weapon objects")

    # Load and filter vehicle weapons
    all_vehicle_weapons_data: List[dict] = load_vehicle_weapons_data_files(
        directory=data_files_directory
    )

    filtered_vehicle_weapons_data: List[dict] = filter_vehicle_weapons(
        all_vehicle_weapons_data
    )

    # Load fire groups
    all_fire_groups_data: List[dict] = load_fire_groups_data_files(
        directory=data_files_directory
    )

    # Generate vehicle weapons
    vehicle_weapons: List[VehicleWeapon] = parse_vehicle_weapons_data(
        vehicle_weapons_data=filtered_vehicle_weapons_data,
        fire_groups_data=all_fire_groups_data,
    )

    print(f"Generated {len(vehicle_weapons)} vehicle weapon objects")

    return vehicle_weapons


def filter_vehicle_weapons(data: List[dict]) -> List[dict]:
    ifw: List[dict] = list(
        filter(lambda x: (int(x["item_id"]) not in EXCLUDED_ITEM_IDS), data)
    )

    return ifw


def parse_vehicle_weapons_data(
    vehicle_weapons_data: List[dict], fire_groups_data: List[dict]
) -> List[VehicleWeapon]:
    vehicle_weapons: List[VehicleWeapon] = []

    fire_groups_id_idx: Dict[int, dict] = {
        int(x["fire_group_id"]): x for x in fire_groups_data
    }

    try:
        d: dict
        for d in vehicle_weapons_data:
            item_id: int = get(d, "item_id", int)

            if item_id in VEHICLE_WEAPONS_DATA_FIXERS:
                VEHICLE_WEAPONS_DATA_FIXERS[item_id](d)

            w: dict = d["item_to_weapon"]["weapon"]
            w_d: dict = d.get("weapon_datasheet", {})

            # Fire groups
            fire_groups: List[FireGroup] = []

            _fg: dict
            for _fg in sorted(
                w["weapon_to_fire_groups"],
                key=lambda x: optget(x, "fire_group_index", int, 0),
            ):
                fg_id: int = get(_fg, "fire_group_id", int)

                fg: dict = fire_groups_id_idx[fg_id]

                fire_groups.append(
                    parse_fire_group_data(
                        fg=fg,
                        ammo_clip_size=optget(w_d, "clip_size", int, 0),
                        ammo_total_capacity=optget(w_d, "capacity", int, 0),
                        heat_overheat_penalty_time=optget(
                            w, "heat_overheat_penalty_ms", int, 0
                        ),
                        heat_bleed_off_rate=optget(w, "heat_bleed_off_rate", int, 0),
                        fire_groups_id_idx=fire_groups_id_idx,
                    )
                )

            # Attachments
            attachments: List[Attachment] = []

            handled_attachments: Set[Tuple[int, int]] = set()

            _at: dict
            for _at in sorted(
                d.get("item_attachments", []),
                key=lambda x: get(x, "attachment_item_id", int),
            ):
                at_item_id: int = get(_at, "item_id", int)
                at_attachment_item_id: int = get(_at, "attachment_item_id", int)

                if (at_item_id, at_attachment_item_id) in handled_attachments:
                    continue

                at: dict = _at["item"]

                attachment_effects: List[dict] = []
                attachment_fire_groups: List[FireGroup] = []

                for zef in at.get("zone_effects", []):
                    p_zef: dict = {}

                    # Effect Type
                    eft: dict = zef["zone_effect_type"]

                    p_zef["action"] = eft["description"]

                    for k, v in eft.items():
                        if k.startswith("string") or k.startswith("param"):
                            if k in zef:
                                p_zef[v] = zef[k]

                    # Handle added fire groups
                    if eft["description"] == "Weapon Add Fire Group":
                        a_fg_id: int = get(p_zef, "FireGroupId", int)

                        a_fg: dict = fire_groups_id_idx[a_fg_id]

                        attachment_fire_groups.append(
                            parse_fire_group_data(
                                fg=a_fg,
                                ammo_clip_size=0,
                                ammo_total_capacity=0,
                                heat_overheat_penalty_time=0,
                                heat_bleed_off_rate=0,
                                fire_groups_id_idx=fire_groups_id_idx,
                            )
                        )

                    attachment_effects.append(p_zef)

                attachment: Attachment = Attachment(
                    item_id=at_item_id,
                    attachment_item_id=at_attachment_item_id,
                    name=at["name"]["en"],
                    description=at.get("description", {"en": None})["en"],
                    slug=slugify(at["name"]["en"]),
                    image_path=at.get("image_path"),
                    is_default=get(at, "is_default_attachment", int) == 1,
                    effects=attachment_effects,
                    fire_groups=attachment_fire_groups,
                )

                attachments.append(attachment)

                handled_attachments.add((at_item_id, at_attachment_item_id))

            # Infantry weapons
            vehicle_weapon: VehicleWeapon = VehicleWeapon(
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
                equip_time=optget(w, "equip_ms", int, 0),
                unequip_time=optget(w, "unequip_ms", int, 0),
                from_ads_time=optget(w, "from_iron_sights_ms", int, 0),
                to_ads_time=optget(w, "to_iron_sights_ms", int, 0),
                sprint_recovery_time=optget(w, "sprint_recovery_ms", int, 0),
                # Fire groups
                fire_groups=fire_groups,
                # Attachments
                attachments=attachments,
            )

            vehicle_weapons.append(vehicle_weapon)

    except (KeyError, ValueError, AssertionError) as e:
        print(f"{item_id}: {d['name']['en']}")
        raise e

    return vehicle_weapons
