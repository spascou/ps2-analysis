import functools
import math
from dataclasses import dataclass

import methodtools


@dataclass
class Heat:
    total_capacity: int
    heat_per_shot: int
    overheat_penalty_time: int
    recovery_delay: int
    recovery_rate: int

    @functools.cached_property
    def shots_before_overheat(self) -> int:

        if self.heat_per_shot == 0:

            return -1

        elif self.total_capacity == 0:

            return 0

        return int(math.floor(self.total_capacity / self.heat_per_shot))

    @functools.cached_property
    def shots_to_overheat(self) -> int:

        if self.shots_before_overheat == -1:

            return -1

        elif self.shots_before_overheat == 0:

            return 0

        return self.shots_before_overheat + 1

    @methodtools.lru_cache()
    def recovery_time(self, heat: int) -> int:

        if heat == 0:

            return 0

        elif self.recovery_rate > 0:

            return self.recovery_delay + int(
                math.ceil(heat / (self.recovery_rate / 1000))
            )

        return -1

    @functools.cached_property
    def full_recovery_time(self) -> int:

        return self.recovery_time(heat=self.total_capacity)

    @functools.cached_property
    def overheat_recovery_time(self) -> int:

        if self.full_recovery_time >= 0:

            return self.overheat_penalty_time + self.full_recovery_time

        return -1
