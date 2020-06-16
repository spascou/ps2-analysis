import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


class DamageLocation(str, Enum):
    HEAD = "head"
    LEGS = "legs"
    TORSO = "torso"


@dataclass
class DamageProfile:
    # Base damage
    max_damage: int
    max_damage_range: float
    min_damage: int
    min_damage_range: float

    # Pellets
    pellets_count: int

    # Locational modifiers
    location_multiplier: Dict[DamageLocation, float] = field(default_factory=dict)

    # Effect
    effect: Dict[str, str] = field(default_factory=dict)

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
            damage = self.min_damage * (
                1
                - (distance - self.min_damage_range)
                / (self.max_damage_range - self.min_damage_range)
            ) + self.max_damage * (
                (distance - self.min_damage_range)
                / (self.max_damage_range - self.min_damage_range)
            )

        return int(math.floor(damage * self.location_multiplier.get(location, 1.0)))

    def damage_per_shot(
        self, distance: float, location: DamageLocation = DamageLocation.TORSO
    ) -> int:

        return self.pellets_count * self.damage_per_pellet(
            distance=distance, location=location
        )
