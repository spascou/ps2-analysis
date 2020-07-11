from dataclasses import dataclass
from typing import Optional

import methodtools


@dataclass
class ConeOfFire:
    max_angle: float
    min_angle: float
    bloom: float
    recovery_rate: float
    recovery_delay: int
    multiplier: float
    moving_multiplier: float
    pellet_spread: float
    grow_rate: Optional[float] = None

    @methodtools.lru_cache()
    def min_cof_angle(self, moving: bool = False) -> float:

        if moving is True:

            return self.min_angle * self.multiplier * self.moving_multiplier

        return self.min_angle * self.multiplier

    @methodtools.lru_cache()
    def max_cof_angle(self, moving: bool = False) -> float:

        if moving is True:

            return self.max_angle * self.multiplier * self.moving_multiplier

        return self.max_angle * self.multiplier

    @methodtools.lru_cache()
    def apply_bloom(self, current: float, moving: bool = False) -> float:

        if current < self.max_cof_angle(moving=moving):

            new: float = current + self.bloom

            return min(new, self.max_cof_angle(moving=moving))

        return self.max_cof_angle(moving=moving)

    @methodtools.lru_cache()
    def recover(self, current: float, time: int, moving: bool = False) -> float:

        if self.recovery_rate > 0:

            new: float = current - (self.recovery_rate / 1_000) * time

            return max(new, self.min_cof_angle(moving=moving))

        return current
