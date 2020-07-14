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
    acceleration: float = 0.0
    turn_rate: Optional[float] = None
    max_speed: Optional[float] = None

    @functools.cached_property
    def max_range(self) -> float:

        if self.life_time >= 0:

            return self.speed * (self.life_time / 1_000)

        return -1
