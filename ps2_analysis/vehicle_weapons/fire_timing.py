import math
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class FireTiming:
    # Basic information
    is_automatic: bool
    refire_time: int
    fire_duration: Optional[int]

    # Burst
    burst_length: Optional[int]
    burst_refire_time: Optional[int]

    # Delay
    delay: int

    # Charge
    charge_up_time: int

    # Spooling
    spool_up_time: Optional[int]
    spool_up_initial_refire_time: Optional[int]

    # Chambering
    chamber_time: Optional[int]

    @property
    def total_delay(self) -> int:

        return (self.delay or 0) + (self.charge_up_time or 0)

    def spooling_refire_time(self, t: int, linear_transition: bool = False) -> int:

        if self.spool_up_time and self.spool_up_initial_refire_time:

            if t < self.spool_up_time:

                # For linear transition
                if linear_transition is True:

                    return int(
                        math.ceil(
                            self.spool_up_initial_refire_time
                            + t
                            * (self.refire_time - self.spool_up_initial_refire_time)
                            / self.spool_up_time
                        )
                    )

                # For step transition
                else:

                    return self.spool_up_initial_refire_time

            else:

                return self.refire_time
        else:

            return self.refire_time

    def generate_shot_timings(
        self, shots: int, control_time: int = 0, spool_cold_start: bool = True
    ) -> List[Tuple[int, bool]]:

        time: int = self.total_delay
        fired_shots: int = 0
        burst_fired_shots: int = 0

        result: List[Tuple[int, bool]] = []

        fired_shots += 1
        result.append((time, True))

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

            # (Semi-)automatic or manual action weapon
            else:

                if not self.is_automatic:

                    first = True
                    time += control_time

                time += self.refire_time + (self.chamber_time or 0)

            fired_shots += 1

            result.append((time, first))

        return result

    def time_to_fire_shots(self, shots: int, spool_cold_start: bool = True) -> int:

        return self.generate_shot_timings(
            shots=shots, spool_cold_start=spool_cold_start
        )[-1][0]
