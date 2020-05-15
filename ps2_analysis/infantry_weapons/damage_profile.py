import math
from enum import Enum
from typing import Dict, Optional


class DamageLocation(str, Enum):
    HEAD = "head"
    LEGS = "legs"
    TORSO = "torso"


class DamageProfile:
    # Base damage
    max_damage: int
    max_damage_range: float
    min_damage: int
    min_damage_range: float

    # Pellets
    pellets_count: int

    # Locational modifiers
    location_multiplier: Dict[DamageLocation, float]

    def __init__(
        self,
        # Base damage
        max_damage: int,
        max_damage_range: float,
        min_damage: int,
        min_damage_range: float,
        # Pellets
        pellets_count: int,
        # Locational modifiers
        location_multiplier: Optional[Dict[DamageLocation, float]] = None,
    ):
        assert pellets_count >= 1
        assert min_damage <= max_damage
        assert min_damage_range >= max_damage_range

        # Base damage
        self.max_damage = max_damage
        self.max_damage_range = max_damage_range
        self.min_damage = min_damage
        self.min_damage_range = min_damage_range

        # Pellets
        self.pellets_count = pellets_count

        # Locational modifiers
        self.location_multiplier = location_multiplier if location_multiplier else {}

    @property
    def damage_delta(self) -> int:
        return self.max_damage - self.min_damage

    @property
    def damage_range_delta(self) -> float:
        return self.min_damage_range - self.max_damage_range

    def damage_per_pellet(
        self, distance: float, location: DamageLocation = DamageLocation.TORSO
    ) -> int:

        damage: float
        if self.damage_range_delta == 0 or distance <= self.max_damage_range:
            damage = self.max_damage
        elif distance >= self.min_damage_range:
            damage = self.min_damage
        else:
            damage = self.max_damage * (
                1
                - (distance - self.min_damage_range)
                / (self.max_damage_range - self.min_damage_range)
            ) + self.min_damage * (
                (distance - self.min_damage_range)
                / (self.max_damage_range - self.min_damage_range)
            )

        return int(math.floor(damage * self.location_multiplier.get(location, 1.0)))

    def damage_per_shot(
        self, distance: int, location: DamageLocation = DamageLocation.TORSO
    ):
        return self.pellets_count * self.damage_per_pellet(
            distance=distance, location=location
        )

    def shots_to_kill(
        self,
        distance: int,
        location: DamageLocation = DamageLocation.TORSO,
        health: int = 500,
        shields: int = 500,
        damage_resistance: float = 0.0,
    ) -> int:
        return int(
            math.ceil(
                (health + shields)
                / (
                    math.ceil(
                        self.damage_per_shot(distance=distance, location=location)
                        * (1 - damage_resistance)
                    )
                )
            )
        )
