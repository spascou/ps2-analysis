from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ps2_census.enums import PlayerState

from ps2_analysis.utils import all_equal

from .ammo import Ammo
from .cone_of_fire import ConeOfFire
from .damage_profile import DamageProfile
from .fire_mode import FireMode
from .fire_timing import FireTiming
from .heat import Heat
from .lock_on import LockOn
from .projectile import Projectile
from .recoil import Recoil


@dataclass
class FireGroup:
    fire_group_id: int
    description: str
    transition_time: int
    fire_modes: List[FireMode] = field(default_factory=list)

    @property
    def fire_timing(self) -> Optional[FireTiming]:
        if self.fire_modes and all_equal((fm.fire_timing for fm in self.fire_modes)):

            return self.fire_modes[0].fire_timing

        else:

            return None

    @property
    def recoil(self) -> Optional[Recoil]:
        if self.fire_modes and all_equal((fm.recoil for fm in self.fire_modes)):

            return self.fire_modes[0].recoil

        else:

            return None

    @property
    def player_state_cone_of_fire(self) -> Optional[Dict[PlayerState, ConeOfFire]]:
        if self.fire_modes and all_equal(
            (fm.player_state_cone_of_fire for fm in self.fire_modes)
        ):

            return self.fire_modes[0].player_state_cone_of_fire

        else:

            return None

    @property
    def player_state_can_ads(self) -> Optional[Dict[PlayerState, bool]]:
        if self.fire_modes and all_equal(
            (fm.player_state_can_ads for fm in self.fire_modes)
        ):

            return self.fire_modes[0].player_state_can_ads

        else:

            return None

    @property
    def projectile(self) -> Optional[Projectile]:
        if self.fire_modes and all_equal((fm.projectile for fm in self.fire_modes)):

            return self.fire_modes[0].projectile

        else:

            return None

    @property
    def lock_on(self) -> Optional[LockOn]:
        if self.fire_modes and all_equal((fm.lock_on for fm in self.fire_modes)):

            return self.fire_modes[0].lock_on

        else:

            return None

    @property
    def direct_damage_profile(self) -> Optional[DamageProfile]:
        if self.fire_modes and all_equal(
            (fm.direct_damage_profile for fm in self.fire_modes)
        ):

            return self.fire_modes[0].direct_damage_profile

        else:

            return None

    @property
    def indirect_damage_profile(self) -> Optional[DamageProfile]:
        if self.fire_modes and all_equal(
            (fm.indirect_damage_profile for fm in self.fire_modes)
        ):

            return self.fire_modes[0].indirect_damage_profile

        else:

            return None

    @property
    def ammo(self) -> Optional[Ammo]:
        if self.fire_modes and all_equal((fm.ammo for fm in self.fire_modes)):

            return self.fire_modes[0].ammo

        else:

            return None

    @property
    def heat(self) -> Optional[Heat]:
        if self.fire_modes and all_equal((fm.heat for fm in self.fire_modes)):

            return self.fire_modes[0].heat

        else:

            return None
