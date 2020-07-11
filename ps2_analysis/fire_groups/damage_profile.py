import functools
import math
from dataclasses import dataclass, field
from typing import Dict, Iterator, Optional, Tuple

import methodtools

from ps2_analysis.enums import DamageLocation
from ps2_analysis.utils import damage_to_kill, float_range, locational_linear_falloff


@dataclass
class DamageProfile:
    max_damage: int
    max_damage_range: float
    min_damage: int
    min_damage_range: float
    pellets_count: int
    location_multiplier: Dict[DamageLocation, float] = field(default_factory=dict)
    effect: Dict[str, str] = field(default_factory=dict)

    @functools.cached_property
    def damage_delta(self) -> int:

        return self.max_damage - self.min_damage

    @functools.cached_property
    def damage_range_delta(self) -> float:

        return self.min_damage_range - self.max_damage_range

    @methodtools.lru_cache()
    def damage_per_pellet(
        self, distance: float, location: DamageLocation = DamageLocation.TORSO
    ) -> int:

        damage: float = locational_linear_falloff(
            x=distance,
            x_0=self.max_damage_range,
            y_0=self.max_damage,
            x_1=self.min_damage_range,
            y_1=self.min_damage,
        )

        return int(math.floor(damage * self.location_multiplier.get(location, 1.0)))

    @methodtools.lru_cache()
    def damage_per_shot(
        self, distance: float, location: DamageLocation = DamageLocation.TORSO
    ) -> int:

        return self.pellets_count * self.damage_per_pellet(
            distance=distance, location=location
        )

    @methodtools.lru_cache()
    def shots_to_kill(
        self,
        distance: float,
        location: DamageLocation = DamageLocation.TORSO,
        health: int = 500,
        shields: int = 500,
        damage_resistance: float = 0.0,
    ) -> int:

        dps: int = self.damage_per_shot(distance=distance, location=location)

        if dps != 0:

            return int(
                math.ceil(
                    damage_to_kill(
                        health=health,
                        shields=shields,
                        damage_resistance=damage_resistance,
                    )
                    / dps
                )
            )

        return -1

    def shots_to_kill_ranges(
        self,
        location: DamageLocation = DamageLocation.TORSO,
        health: int = 500,
        shields: int = 500,
        damage_resistance: float = 0.0,
        step: float = 0.1,
        precision_decimals: int = 2,
    ) -> Iterator[Tuple[float, int]]:

        if self.damage_range_delta > 0:

            previous_stk: Optional[int] = None

            for r in float_range(
                0.0, self.min_damage_range + step, step, precision_decimals
            ):

                stk: int = self.shots_to_kill(
                    distance=r,
                    location=location,
                    health=health,
                    shields=shields,
                    damage_resistance=damage_resistance,
                )

                if previous_stk is None or stk != previous_stk:

                    if r >= step:

                        yield (round(r - step, precision_decimals), stk)

                    else:

                        yield (r, stk)

                previous_stk = stk

        else:

            yield (
                0.0,
                self.shots_to_kill(
                    distance=self.max_damage_range,
                    location=location,
                    health=health,
                    shields=shields,
                    damage_resistance=damage_resistance,
                ),
            )
