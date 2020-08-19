from dataclasses import dataclass
from typing import Optional

import methodtools

from ps2_analysis.utils import fastround


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
    def min_cof_angle(self, moving: bool = False, precision_decimals: int = 6) -> float:

        result: float = self.min_angle * self.multiplier

        if moving is True:

            result *= self.moving_multiplier

        return fastround(result, precision_decimals)

    @methodtools.lru_cache()
    def max_cof_angle(self, moving: bool = False, precision_decimals: int = 6) -> float:

        result: float = self.max_angle * self.multiplier

        if moving is True:

            result *= self.moving_multiplier

        return fastround(result, precision_decimals)

    @methodtools.lru_cache()
    def apply_bloom(
        self, current: float, moving: bool = False, precision_decimals: int = 6
    ) -> float:

        if current < self.max_cof_angle(
            moving=moving, precision_decimals=precision_decimals
        ):

            new: float = fastround(current + self.bloom, precision_decimals)

            return min(
                new,
                self.max_cof_angle(
                    moving=moving, precision_decimals=precision_decimals
                ),
            )

        return self.max_cof_angle(moving=moving)

    @methodtools.lru_cache()
    def recover(
        self,
        current: float,
        time: int,
        moving: bool = False,
        precision_decimals: int = 6,
    ) -> float:

        if self.recovery_rate > 0:

            new: float = fastround(
                current - (self.recovery_rate / 1_000) * time, precision_decimals
            )

            return max(new, self.min_cof_angle(moving=moving))

        return current
