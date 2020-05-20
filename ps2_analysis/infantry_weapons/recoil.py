import math
from typing import Optional


class Recoil:
    # Angle
    max_angle: float
    min_angle: float

    # Vertical
    max_vertical: float
    min_vertical: float
    vertical_increase: float
    vertical_crouched_increase: float

    # Horizontal
    max_horizontal: float
    min_horizontal: float
    horizontal_tolerance: Optional[float]
    max_horizontal_increase: float
    min_horizontal_increase: float

    # Recovery
    recovery_acceleration: float
    recovery_delay: int
    recovery_rate: float

    # Misc
    first_shot_multiplier: float
    shots_at_min_magnitude: Optional[int]
    max_total_magnitude: Optional[float]

    def __init__(
        self,
        # Angle
        max_angle: float,
        min_angle: float,
        # Vertical
        max_vertical: float,
        min_vertical: float,
        vertical_increase: float,
        vertical_crouched_increase: float,
        # Horizontal
        max_horizontal: float,
        min_horizontal: float,
        horizontal_tolerance: Optional[float],
        max_horizontal_increase: float,
        min_horizontal_increase: float,
        # Recovery
        recovery_acceleration: float,
        recovery_rate: float,
        recovery_delay: int,
        # Misc
        first_shot_multiplier: float,
        shots_at_min_magnitude: Optional[int] = None,
        max_total_magnitude: Optional[float] = None,
    ):
        assert min_angle <= max_angle
        assert min_vertical <= max_vertical
        assert min_horizontal <= max_horizontal

        # Angle
        self.max_angle = max_angle
        self.min_angle = min_angle

        # Vertical
        self.max_vertical = max_vertical
        self.min_vertical = min_vertical
        self.vertical_increase = vertical_increase
        self.crouched_vertical_increase = vertical_crouched_increase

        # Horizontal
        self.max_horizontal = max_horizontal
        self.min_horizontal = min_horizontal
        self.horizontal_tolerance = horizontal_tolerance
        self.max_horizontal_increase = max_horizontal_increase
        self.min_horizontal_increase = min_horizontal_increase

        # Recovery
        self.recovery_acceleration = recovery_acceleration
        self.recovery_delay = recovery_delay
        self.recovery_rate = recovery_rate

        # Misc
        self.first_shot_multiplier = first_shot_multiplier
        self.shots_at_min_magnitude = shots_at_min_magnitude
        self.max_total_magnitude = max_total_magnitude

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
            if self.min_horizontal > 0:
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
        if self.max_tolerated_horizontal_kicks:
            res = self.max_tolerated_horizontal_kicks * self.max_horizontal * 2
            return res
        else:
            return None

    @property
    def horizontal_delta(self) -> float:
        res = self.max_horizontal - self.min_horizontal
        return res

    @property
    def vertical_delta(self) -> float:
        res = self.max_vertical - self.min_vertical
        return res
