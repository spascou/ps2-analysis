import functools
import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class Ammo:
    clip_size: int
    total_capacity: int
    ammo_per_shot: int
    short_reload_time: int
    reload_chamber_time: int
    block_auto: Optional[bool] = None
    continuous: Optional[bool] = None
    loop_start_time: Optional[int] = None
    loop_end_time: Optional[int] = None

    @functools.cached_property
    def shots_per_clip(self) -> int:

        if self.ammo_per_shot == 0:

            return -1

        elif self.clip_size == 0:

            return 0

        return int(math.floor(self.clip_size / self.ammo_per_shot))

    @functools.cached_property
    def long_reload_time(self) -> int:

        if self.loop_start_time and self.loop_end_time:

            return (
                self.loop_start_time
                + self.clip_size * self.short_reload_time
                + self.loop_end_time
                + self.reload_chamber_time
            )

        return self.short_reload_time + self.reload_chamber_time
