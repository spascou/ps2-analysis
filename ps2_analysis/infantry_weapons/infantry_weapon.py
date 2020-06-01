from dataclasses import dataclass, field
from typing import List, Optional

from ps2_census.enums import Faction, ItemCategory

from .attachment import Attachment
from .fire_group import FireGroup


@dataclass
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
    fire_groups: List[FireGroup] = field(default_factory=list)

    # Attachments
    attachments: List[Attachment] = field(default_factory=list)
