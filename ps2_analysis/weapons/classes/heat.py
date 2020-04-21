import math


class Heat:
    # Basic information
    total_capacity: int
    heat_per_shot: int

    # Heat management
    overheat_penalty_time: int
    recovery_delay: int
    recovery_rate: int
    threshold: int

    def __init__(
        self,
        # Basic information
        total_capacity: int,
        heat_per_shot: int,
        # Heat management
        overheat_penalty_time: int,
        recovery_delay: int,
        recovery_rate: int,
        threshold: int,
    ):
        # Basic information
        self.total_capacity = total_capacity
        self.heat_per_shot = heat_per_shot

        # Heat management
        self.overheat_penalty_time = overheat_penalty_time
        self.recovery_delay = recovery_delay
        self.recovery_rate = recovery_rate
        self.threshold = threshold

    @property
    def shots_before_overheat(self) -> int:
        return int(math.floor(self.total_capacity / self.heat_per_shot))

    @property
    def shots_to_overheat(self) -> int:
        return self.shots_before_overheat + 1

    def recovery_time(self, heat: int) -> int:
        return self.recovery_delay + int(math.ceil(heat / (self.recovery_rate / 1000)))

    @property
    def full_recovery_time(self) -> int:
        return self.recovery_time(heat=self.total_capacity)

    @property
    def overheat_recovery_time(self) -> int:
        return self.overheat_penalty_time + self.full_recovery_time
