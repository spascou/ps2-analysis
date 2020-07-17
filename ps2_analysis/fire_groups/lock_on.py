from dataclasses import dataclass
from typing import Optional


@dataclass
class LockOn:
    life_time: int
    seek_in_flight: bool
    maintain: bool
    required: bool
    turn_rate: Optional[float] = None
