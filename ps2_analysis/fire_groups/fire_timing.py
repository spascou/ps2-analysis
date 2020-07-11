import functools
from dataclasses import dataclass
from typing import Iterator, Optional, Tuple

import methodtools


@dataclass
class FireTiming:
    is_automatic: bool
    refire_time: int
    fire_duration: int
    delay: int
    charge_up_time: int
    burst_length: Optional[int] = None
    burst_refire_time: Optional[int] = None
    spool_up_time: Optional[int] = None
    spool_up_initial_refire_time: Optional[int] = None
    chamber_time: Optional[int] = None

    @functools.cached_property
    def total_delay(self) -> int:

        return (self.delay or 0) + (self.charge_up_time or 0)

    @methodtools.lru_cache()
    def spooling_refire_time(self, t: int) -> int:

        if self.spool_up_time and self.spool_up_initial_refire_time:

            if t < self.spool_up_time:

                return self.spool_up_initial_refire_time

            return self.refire_time

        return self.refire_time

    def generate_shot_timings(
        self,
        shots: int = -1,
        control_time: int = 0,
        auto_burst_length: Optional[int] = None,
        spool_cold_start: bool = True,
    ) -> Iterator[Tuple[int, bool]]:

        if shots == 0:

            yield (0, False)

            return

        time: int = self.total_delay
        fired_shots: int = 0
        burst_fired_shots: int = 0

        fired_shots += 1

        yield (time, True)

        while fired_shots < shots:

            first: bool = False

            # Spooling weapon
            if (
                self.spool_up_time
                and self.spool_up_initial_refire_time
                and spool_cold_start
            ):

                time += self.spooling_refire_time(time - self.total_delay)

            # Bursting weapon
            elif self.burst_length and self.burst_length > 1 and self.burst_refire_time:

                if burst_fired_shots < self.burst_length - 1:

                    burst_fired_shots += 1
                    time += self.burst_refire_time

                else:

                    first = True
                    burst_fired_shots = 0
                    time += control_time
                    time += self.refire_time + self.total_delay

            # Manually bursting automatic weapon
            elif auto_burst_length and auto_burst_length > 1 and control_time:

                if burst_fired_shots < auto_burst_length - 1:

                    burst_fired_shots += 1
                    time += self.refire_time

                else:

                    first = True
                    burst_fired_shots = 0
                    time += control_time
                    time += self.refire_time

            else:

                # (Semi-)automatic or manual action weapon
                if not self.is_automatic:

                    first = True
                    time += control_time

                time += self.refire_time + (self.chamber_time or 0)

            fired_shots += 1

            yield (time, first)

    @methodtools.lru_cache()
    def time_to_fire_shots(self, shots: int, spool_cold_start: bool = True) -> int:

        return list(
            self.generate_shot_timings(shots=shots, spool_cold_start=spool_cold_start)
        )[-1][0]
