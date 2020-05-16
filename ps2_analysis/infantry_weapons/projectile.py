from typing import Optional

from ps2_census.enums import ProjectileFlightType


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

    def __init__(
        self,
        # Speed
        speed: float,
        max_speed: Optional[float],
        acceleration: Optional[float],
        # Trajectory
        flight_type: ProjectileFlightType,
        gravity: Optional[float],
        turn_rate: Optional[float],
        # Misc
        life_time: int,
        drag: Optional[float],
    ):
        # Speed
        self.speed = speed
        self.max_speed = max_speed
        self.acceleration = acceleration

        # Trajectory
        self.flight_type = flight_type
        self.gravity = gravity
        self.turn_rate = turn_rate

        # Misc
        self.life_time = life_time
        self.drag = drag

    @property
    def max_range(self) -> float:
        return self.speed * (self.life_time / 1_000)
