from dataclasses import dataclass, field
from typing import List, Optional

from ps2_census.enums import Faction, ItemCategory

from ps2_analysis.fire_groups.fire_group import FireGroup
from ps2_analysis.weapons.attachment import Attachment


@dataclass
class VehicleWeapon:
    item_id: int
    weapon_id: int
    name: str
    description: str
    slug: str
    faction: Faction
    category: ItemCategory
    move_multiplier: float
    turn_multiplier: float
    equip_time: int
    unequip_time: int
    from_ads_time: int
    to_ads_time: int
    sprint_recovery_time: int
    image_path: Optional[str] = None
    fire_groups: List[FireGroup] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)
