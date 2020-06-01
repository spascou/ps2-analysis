import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


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

    def shots_to_kill(
        self,
        distance: float,
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

    def shots_to_kill_ranges(
        self,
        location: DamageLocation = DamageLocation.TORSO,
        health: int = 500,
        shields: int = 500,
        damage_resistance: float = 0.0,
    ) -> List[Tuple[int, int]]:

        stk_ranges: List[Tuple[int, int]] = []

        if self.damage_range_delta == 0:

            stk_ranges.append(
                (
                    int(math.ceil(self.min_damage_range)),
                    self.shots_to_kill(
                        distance=int(math.ceil(self.min_damage_range)),
                        location=location,
                        health=health,
                        shields=shields,
                        damage_resistance=damage_resistance,
                    ),
                )
            )

        else:

            previous_stk: Optional[int] = None

            r: int
            for r in range(0, int(math.ceil(self.min_damage_range) + 1)):
                stk: int = self.shots_to_kill(
                    distance=r + 0.1,
                    location=location,
                    health=health,
                    shields=shields,
                    damage_resistance=damage_resistance,
                )

                if previous_stk is None or stk != previous_stk:
                    stk_ranges.append((r, stk))

                previous_stk = stk

        return stk_ranges
