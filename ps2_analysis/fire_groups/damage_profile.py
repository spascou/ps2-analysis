import functools
import math
from dataclasses import dataclass, field
from typing import Dict, Iterator, Optional, Tuple

import methodtools
from ps2_census.enums import ResistType

from ps2_analysis.enums import DamageLocation, DamageTargetType
from ps2_analysis.utils import (
    apply_damage_resistance,
    float_range,
    locational_linear_falloff,
    resolve_damage_resistance,
    resolve_health_pool,
)


@dataclass
class DamageProfile:
    max_damage: int
    max_damage_range: float
    min_damage: int
    min_damage_range: float
    pellets_count: int
    resist_type: ResistType
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
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        # Damage degradation due to range is rounded down
        damage: int = int(
            math.floor(
                locational_linear_falloff(
                    x=distance,
                    x_0=self.max_damage_range,
                    y_0=self.max_damage,
                    x_1=self.min_damage_range,
                    y_1=self.min_damage,
                )
            )
        )

        damage_resistance: float = resolve_damage_resistance(
            damage_target_type=damage_target_type,
            damage_location=damage_location,
            resist_type=self.resist_type,
        )

        if damage_resistance < 1.0:

            return apply_damage_resistance(
                damage=math.ceil(
                    damage * self.location_multiplier.get(damage_location, 1.0)
                ),
                resistance=damage_resistance,
            )

        else:

            return 0

    @methodtools.lru_cache()
    def damage_per_shot(
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        return self.pellets_count * self.damage_per_pellet(
            distance=distance,
            damage_target_type=damage_target_type,
            damage_location=damage_location,
        )

    @methodtools.lru_cache()
    def shots_to_kill(
        self,
        distance: float,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
    ) -> int:

        dps: int = self.damage_per_shot(
            distance=distance,
            damage_target_type=damage_target_type,
            damage_location=damage_location,
        )

        if dps > 0:

            return int(
                math.ceil(
                    resolve_health_pool(damage_target_type=damage_target_type) / dps
                )
            )

        return -1

    def shots_to_kill_ranges(
        self,
        damage_target_type: DamageTargetType = DamageTargetType.INFANTRY_BASELINE,
        damage_location: DamageLocation = DamageLocation.TORSO,
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
                    damage_target_type=damage_target_type,
                    damage_location=damage_location,
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
                    damage_target_type=damage_target_type,
                    damage_location=damage_location,
                ),
            )
