import functools
from dataclasses import dataclass
from typing import Optional

from ps2_census.enums import ProjectileFlightType


@dataclass
class Projectile:
    speed: float
    gravity: float
    life_time: int
    flight_type: ProjectileFlightType
    drag: float
    max_speed: Optional[float] = None
    acceleration: Optional[float] = None
    turn_rate: Optional[float] = None

    @functools.cached_property
    def max_range(self) -> float:

        if self.life_time:

            return self.speed * (self.life_time / 1_000)

        return -1
