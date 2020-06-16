from dataclasses import dataclass
from typing import Optional

from ps2_census.enums import ProjectileFlightType


@dataclass
class Projectile:
    # Speed
    speed: float
    max_speed: Optional[float]
    acceleration: Optional[float]

    # Trajectory
    flight_type: ProjectileFlightType
    gravity: Optional[float]
    turn_rate: Optional[float]

    # Misc
    life_time: int
    drag: Optional[float]

    @property
    def max_range(self) -> float:

        return self.speed * (self.life_time / 1_000)
