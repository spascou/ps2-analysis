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
    lockon_turn_rate: Optional[float] = None
    lockon_life_time: Optional[int] = None
    lockon_acceleration: Optional[float] = None
    lockon_lose_angle: Optional[float] = None
    lockon_seek_in_flight: Optional[bool] = None

    @functools.cached_property
    def max_range(self) -> float:

        if self.life_time >= 0:

            return self.speed * (self.life_time / 1_000)

        return -1
