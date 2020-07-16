from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ps2_census.enums import PlayerState

from ps2_analysis.fire_groups.ammo import Ammo
from ps2_analysis.fire_groups.cone_of_fire import ConeOfFire
from ps2_analysis.fire_groups.damage_profile import DamageProfile
from ps2_analysis.fire_groups.fire_group import FireGroup
from ps2_analysis.fire_groups.fire_timing import FireTiming
from ps2_analysis.fire_groups.heat import Heat
from ps2_analysis.fire_groups.lock_on import LockOn
from ps2_analysis.fire_groups.projectile import Projectile
from ps2_analysis.fire_groups.recoil import Recoil
from ps2_analysis.utils import all_equal


@dataclass
class Attachment:
    item_id: int
    attachment_item_id: int
    name: str
    description: str
    slug: str
    is_default: bool
    image_path: Optional[str] = None
    effects: List[Dict[str, str]] = field(default_factory=list)
    fire_groups: List[FireGroup] = field(default_factory=list)

    @property
    def fire_timing(self) -> Optional[FireTiming]:
        if self.fire_groups and all_equal((fg.fire_timing for fg in self.fire_groups)):

            return self.fire_groups[0].fire_timing

        else:

            return None

    @property
    def recoil(self) -> Optional[Recoil]:
        if self.fire_groups and all_equal((fg.recoil for fg in self.fire_groups)):

            return self.fire_groups[0].recoil

        else:

            return None

    @property
    def player_state_cone_of_fire(self) -> Optional[Dict[PlayerState, ConeOfFire]]:
        if self.fire_groups and all_equal(
            (fg.player_state_cone_of_fire for fg in self.fire_groups)
        ):

            return self.fire_groups[0].player_state_cone_of_fire

        else:

            return None

    @property
    def player_state_can_ads(self) -> Optional[Dict[PlayerState, bool]]:
        if self.fire_groups and all_equal(
            (fg.player_state_can_ads for fg in self.fire_groups)
        ):

            return self.fire_groups[0].player_state_can_ads

        else:

            return None

    @property
    def projectile(self) -> Optional[Projectile]:
        if self.fire_groups and all_equal((fg.projectile for fg in self.fire_groups)):

            return self.fire_groups[0].projectile

        else:

            return None

    @property
    def lock_on(self) -> Optional[LockOn]:
        if self.fire_groups and all_equal((fg.lock_on for fg in self.fire_groups)):

            return self.fire_groups[0].lock_on

        else:

            return None

    @property
    def direct_damage_profile(self) -> Optional[DamageProfile]:
        if self.fire_groups and all_equal(
            (fg.direct_damage_profile for fg in self.fire_groups)
        ):

            return self.fire_groups[0].direct_damage_profile

        else:

            return None

    @property
    def indirect_damage_profile(self) -> Optional[DamageProfile]:
        if self.fire_groups and all_equal(
            (fg.indirect_damage_profile for fg in self.fire_groups)
        ):

            return self.fire_groups[0].indirect_damage_profile

        else:

            return None

    @property
    def ammo(self) -> Optional[Ammo]:
        if self.fire_groups and all_equal((fg.ammo for fg in self.fire_groups)):

            return self.fire_groups[0].ammo

        else:

            return None

    @property
    def heat(self) -> Optional[Heat]:
        if self.fire_groups and all_equal((fg.heat for fg in self.fire_groups)):

            return self.fire_groups[0].heat

        else:

            return None
