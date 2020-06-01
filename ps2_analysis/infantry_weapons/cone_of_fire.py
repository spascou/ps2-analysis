from dataclasses import dataclass
from typing import Optional


@dataclass
class ConeOfFire:
    # Basic information
    max_angle: float
    min_angle: float
    bloom: float

    # Recovery
    recovery_rate: Optional[float]
    recovery_delay: Optional[int]
    recovery_delay_threshold: Optional[int]

    # Multipliers
    multiplier: float
    moving_multiplier: float

    # Pellet
    pellet_spread: Optional[float]

    # Misc
    grow_rate: Optional[float]
    shots_before_penalty: Optional[int]
    turn_penalty: Optional[float]
    range: float
