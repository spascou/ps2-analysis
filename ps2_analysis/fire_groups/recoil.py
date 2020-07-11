import functools
import math
from dataclasses import dataclass
from typing import Optional, Tuple

import methodtools


@dataclass
class Recoil:
    max_angle: float
    min_angle: float
    max_vertical: float
    min_vertical: float
    vertical_increase: float
    vertical_crouched_increase: float
    max_horizontal: float
    min_horizontal: float
    max_horizontal_increase: float
    min_horizontal_increase: float
    recovery_delay: int
    recovery_rate: float
    first_shot_multiplier: float
    horizontal_tolerance: Optional[float] = None
    recovery_acceleration: Optional[float] = None
    shots_at_min_magnitude: Optional[int] = None
    max_total_magnitude: Optional[float] = None

    @functools.cached_property
    def half_horizontal_tolerance(self) -> Optional[float]:

        if self.horizontal_tolerance is not None:

            return self.horizontal_tolerance / 2

        return None

    @functools.cached_property
    def max_tolerated_horizontal_kicks(self) -> int:

        if self.half_horizontal_tolerance is not None:

            if self.min_horizontal != 0:

                return (
                    int(
                        math.floor(self.half_horizontal_tolerance / self.min_horizontal)
                    )
                    + 1
                )

            return -1

        return -1

    @functools.cached_property
    def max_horizontal_deviation(self) -> float:

        if self.max_tolerated_horizontal_kicks == -1:

            return -1

        return self.max_tolerated_horizontal_kicks * self.max_horizontal * 2

    @functools.cached_property
    def angle_delta(self) -> float:

        return self.max_angle - self.min_angle

    @functools.cached_property
    def horizontal_delta(self) -> float:

        return self.max_horizontal - self.min_horizontal

    @functools.cached_property
    def vertical_delta(self) -> float:

        return self.max_vertical - self.min_vertical

    @methodtools.lru_cache()
    def scale_vertical(
        self, current_min: float, current_max: float
    ) -> Tuple[float, float]:

        new_min: float = current_min
        new_max: float = current_max

        if self.vertical_increase > 0:

            if current_min < current_max:

                new_min = current_min + self.vertical_increase
                new_min = min(new_min, current_max)

        elif self.vertical_increase < 0:

            if current_max > current_min:

                new_max = current_max + self.vertical_increase
                new_max = max(current_min, new_max)

        return (new_min, new_max)

    @methodtools.lru_cache()
    def scale_min_horizontal(self, current_min: float, current_max: float) -> float:

        new: float

        if self.min_horizontal_increase < 0:

            if current_min > 0:

                new = current_min + self.min_horizontal_increase

                return max(0.0, new)

        elif self.min_horizontal_increase > 0:

            if current_min < current_max:

                new = current_min + self.min_horizontal_increase

                return min(new, current_max)

        return current_min

    @methodtools.lru_cache()
    def scale_max_horizontal(self, current_min: float, current_max: float) -> float:

        new: float

        if self.max_horizontal_increase > 0:

            return current_max + self.max_horizontal_increase

        elif self.max_horizontal_increase < 0:

            new = current_max + self.max_horizontal_increase

            return max(current_min, new)

        return current_max

    @methodtools.lru_cache()
    def scale_horizontal(
        self, current_min: float, current_max: float
    ) -> Tuple[float, float]:

        return (
            self.scale_min_horizontal(current_min=current_min, current_max=current_max),
            self.scale_max_horizontal(current_min=current_min, current_max=current_max),
        )

    @methodtools.lru_cache()
    def recover(
        self, current_x: float, current_y: float, time: int, moving: bool = False
    ) -> Tuple[float, float]:

        if self.recovery_rate > 0:

            full_recovery_time: int = int(
                math.ceil(
                    math.sqrt(current_x ** 2 + current_y ** 2)
                    / (self.recovery_rate / 1_000)
                )
            )

            if time < full_recovery_time:

                r: float = math.atan(current_x / current_y)

                new_x = current_x - (time * (self.recovery_rate / 1_000) * math.sin(r))
                new_y = current_y - (time * (self.recovery_rate / 1_000) * math.cos(r))

                return (new_x, new_y)

            else:

                return (0.0, 0.0)

        return (current_x, current_y)
