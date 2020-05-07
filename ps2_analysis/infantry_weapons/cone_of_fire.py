from typing import Optional


class ConeOfFire:
    # Basic information
    max_angle: float
    min_angle: float
    bloom: float

    # Recovery
    recovery_delay: int
    recovery_rate: float
    recovery_delay_threshold: int

    # Multipliers
    multiplier: float
    moving_multiplier: float

    # Pellet
    pellet_spread: Optional[float]

    # Misc
    grow_rate: float
    shots_before_penalty: int
    turn_penalty: float
    range: float

    def __init__(
        self,
        # Basic information
        max_angle: float,
        min_angle: float,
        bloom: float,
        # Recovery
        recovery_rate: float,
        recovery_delay: int,
        recovery_delay_threshold: int,
        # Multipliers
        multiplier: float,
        moving_multiplier: float,
        # Pellet
        pellet_spread: Optional[float],
        # Misc
        grow_rate: float,
        shots_before_penalty: int,
        turn_penalty: float,
        range: float,
    ):
        assert min_angle <= max_angle

        # Basic information
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.bloom = bloom

        # Recovery
        self.recovery_delay = recovery_delay
        self.recovery_rate = recovery_rate
        self.recovery_delay_threshold = recovery_delay_threshold

        # Multipliers
        self.multiplier = multiplier
        self.moving_multiplier = moving_multiplier

        # Pellet
        self.pellet_spread = pellet_spread

        # Misc
        self.grow_rate = grow_rate
        self.shots_before_penalty = shots_before_penalty
        self.turn_penalty = turn_penalty
        self.range = range
