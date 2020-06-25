import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class Recoil:
    # Angle
    max_angle: Optional[float]
    min_angle: Optional[float]

    # Vertical
    max_vertical: Optional[float]
    min_vertical: Optional[float]
    vertical_increase: float
    vertical_crouched_increase: float

    # Horizontal
    max_horizontal: Optional[float]
    min_horizontal: Optional[float]
    horizontal_tolerance: Optional[float]
    max_horizontal_increase: float
    min_horizontal_increase: float

    # Recovery
    recovery_acceleration: Optional[float]
    recovery_delay: int
    recovery_rate: Optional[float]

    # Misc
    first_shot_multiplier: float
    shots_at_min_magnitude: Optional[int] = None
    max_total_magnitude: Optional[float] = None

    @property
    def half_horizontal_tolerance(self) -> Optional[float]:

        if self.horizontal_tolerance:

            res = self.horizontal_tolerance / 2

            return res

        else:

            return None

    @property
    def max_tolerated_horizontal_kicks(self) -> Optional[int]:

        if self.half_horizontal_tolerance:

            if self.min_horizontal and self.min_horizontal > 0:

                return (
                    int(
                        math.floor(self.half_horizontal_tolerance / self.min_horizontal)
                    )
                    + 1
                )

            else:

                return None

        else:

            return None

    @property
    def max_horizontal_deviation(self) -> Optional[float]:

        if self.max_horizontal and self.max_tolerated_horizontal_kicks:

            res = self.max_tolerated_horizontal_kicks * self.max_horizontal * 2

            return res

        else:

            return None

    @property
    def horizontal_delta(self) -> Optional[float]:

        if self.max_horizontal and self.min_horizontal:

            res = self.max_horizontal - self.min_horizontal

            return res

        else:

            return None

    @property
    def vertical_delta(self) -> Optional[float]:

        if self.max_vertical and self.min_vertical:

            res = self.max_vertical - self.min_vertical

            return res

        else:

            return None
