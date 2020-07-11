from typing import Dict, FrozenSet, Iterator, List, Set, Tuple

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


def generate_all_vehicle_weapons(
    data_files_directory: str, no_children: bool = False
) -> Iterator[VehicleWeapon]:
    print("Generating vehicle weapon objects")

    # Load and filter vehicle weapons
    all_vehicle_weapons_data: List[dict] = list(
        load_vehicle_weapons_data_files(directory=data_files_directory)
    )

    # Load fire groups
    all_fire_groups_data: List[dict] = list(
        load_fire_groups_data_files(directory=data_files_directory)
    )

    # Index fire groups data by ID
    all_fire_groups_data_id_idx: Dict[int, dict] = {
        int(x["fire_group_id"]): x for x in all_fire_groups_data
    }

    # Generate vehicle weapons
    yield from (
        parse_vehicle_weapon_data(
            data=data,
            fire_groups_data_id_idx=all_fire_groups_data_id_idx,
            no_children=no_children,
        )
        for data in filter(
            lambda x: (int(x["item_id"]) not in EXCLUDED_ITEM_IDS),
            all_vehicle_weapons_data,
        )
    )


def parse_vehicle_weapon_data(
    data: dict, fire_groups_data_id_idx: Dict[int, dict], no_children: bool = False
) -> VehicleWeapon:

    try:
        item_id: int = get(data, "item_id", int)

        if item_id in VEHICLE_WEAPONS_DATA_FIXERS:
            VEHICLE_WEAPONS_DATA_FIXERS[item_id](data)

        w: dict = data["item_to_weapon"]["weapon"]
        w_d: dict = data.get("weapon_datasheet", {})

        # Fire groups
        fire_groups: List[FireGroup] = []

        if no_children is False:

            _fg: dict
            for _fg in sorted(
                w["weapon_to_fire_groups"],
                key=lambda x: optget(x, "fire_group_index", int, 0),
            ):
                fg_id: int = get(_fg, "fire_group_id", int)

                fg: dict = fire_groups_data_id_idx[fg_id]

                fire_groups.append(
                    parse_fire_group_data(
                        fg=fg,
                        ammo_clip_size=optget(w_d, "clip_size", int, 0),
                        ammo_total_capacity=optget(w_d, "capacity", int, 0),
                        heat_overheat_penalty_time=optget(
                            w, "heat_overheat_penalty_ms", int, 0
                        ),
                        heat_bleed_off_rate=optget(w, "heat_bleed_off_rate", int, 0),
                    )
                )

        # Attachments
        attachments: List[Attachment] = []

        if no_children is False:

            handled_attachments: Set[Tuple[int, int]] = set()

            _at: dict
            for _at in sorted(
                data.get("item_attachments", []),
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

                        a_fg: dict = fire_groups_data_id_idx[a_fg_id]

                        attachment_fire_groups.append(
                            parse_fire_group_data(
                                fg=a_fg,
                                ammo_clip_size=0,
                                ammo_total_capacity=0,
                                heat_overheat_penalty_time=0,
                                heat_bleed_off_rate=0,
                            )
                        )

                    attachment_effects.append(p_zef)

                attachment: Attachment = Attachment(
                    item_id=at_item_id,
                    attachment_item_id=at_attachment_item_id,
                    name=at["name"]["en"],
                    description=at.get("description", {"en": ""})["en"],
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
            item_id=item_id,
            weapon_id=get(w, "weapon_id", int),
            name=data["name"]["en"],
            description=data["description"]["en"],
            slug=slugify(data["name"]["en"]),
            image_path=data.get("image_path"),
            faction=Faction(optget(data, "faction_id", int, 0)),
            category=ItemCategory(get(data, "item_category_id", int)),
            move_multiplier=get(w, "move_modifier", float),
            turn_multiplier=get(w, "turn_modifier", float),
            equip_time=optget(w, "equip_ms", int, 0),
            unequip_time=optget(w, "unequip_ms", int, 0),
            from_ads_time=optget(w, "from_iron_sights_ms", int, 0),
            to_ads_time=optget(w, "to_iron_sights_ms", int, 0),
            sprint_recovery_time=optget(w, "sprint_recovery_ms", int, 0),
            fire_groups=fire_groups,
            attachments=attachments,
        )

    except (KeyError, ValueError, AssertionError) as e:
        print(f"{item_id}: {data['name']['en']}")
        raise e

    return vehicle_weapon
