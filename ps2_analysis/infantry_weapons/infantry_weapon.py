from typing import List, Optional

from ps2_census.enums import Faction, ItemCategory

from .attachment import Attachment
from .fire_group import FireGroup


class InfantryWeapon:
    # Basic information
    item_id: int
    weapon_id: int
    name: str
    description: str
    slug: str
    image_path: Optional[str]
    faction: Faction
    category: ItemCategory

    # Movement modifiers
    move_multiplier: float
    turn_multiplier: float

    # Handling timings
    equip_time: int
    unequip_time: int
    from_ads_time: int
    to_ads_time: int
    sprint_recovery_time: int

    # Fire groups
    fire_groups: List[FireGroup]

    # Attachments
    attachments: List[Attachment]

    def __init__(
        self,
        # Basic information
        item_id: int,
        weapon_id: int,
        name: str,
        description: str,
        slug: str,
        image_path: Optional[str],
        faction: Faction,
        category: ItemCategory,
        # Movement modifiers
        move_multiplier: float,
        turn_multiplier: float,
        # Handling timings
        equip_time: int,
        unequip_time: int,
        from_ads_time: int,
        to_ads_time: int,
        sprint_recovery_time: int,
        # Fire groups
        fire_groups: Optional[List[FireGroup]] = None,
        # Attachments
        attachments: Optional[List[Attachment]] = None,
    ):
        # Basic information
        self.item_id = item_id
        self.weapon_id = weapon_id
        self.name = name
        self.description = description
        self.slug = slug
        self.image_path = image_path
        self.faction = faction
        self.category = category

        # Movement modifiers
        self.move_multiplier = move_multiplier
        self.turn_multiplier = turn_multiplier

        # Handling timings
        self.equip_time = equip_time
        self.unequip_time = unequip_time
        self.from_ads_time = from_ads_time
        self.to_ads_time = to_ads_time
        self.sprint_recovery_time = sprint_recovery_time

        # Fire groups
        self.fire_groups = fire_groups or []

        # Attachments
        self.attachments = attachments or []
