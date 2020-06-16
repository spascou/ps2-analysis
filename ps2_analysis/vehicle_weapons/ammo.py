import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class Ammo:
    # Basic information
    clip_size: int
    total_capacity: int
    ammo_per_shot: int
    block_auto: Optional[bool]
    continuous: Optional[bool]

    # Reload timing
    short_reload_time: int
    reload_chamber_time: int
    loop_start_time: Optional[int]
    loop_end_time: Optional[int]

    # Chambering
    can_chamber_in_ads: Optional[bool]

    @property
    def shots_per_clip(self) -> int:

        return int(math.floor(self.clip_size / self.ammo_per_shot))

    @property
    def long_reload_time(self) -> int:

        if self.loop_start_time and self.loop_end_time:

            return (
                self.loop_start_time
                + self.clip_size * self.short_reload_time
                + self.loop_end_time
                + self.reload_chamber_time
            )

        else:

            return self.short_reload_time + self.reload_chamber_time
