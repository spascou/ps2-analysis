from dataclasses import dataclass
from typing import Optional


@dataclass
class LockOn:
    life_time: int
    seek_in_flight: bool
    maintain: bool
    required: bool
    acceleration: float = 0.0
    turn_rate: Optional[float] = None
    lose_time: Optional[int] = None
    acquire_time: Optional[int] = None
    acquire_close_time: Optional[int] = None
    acquire_far_time: Optional[int] = None
    range: Optional[float] = None
    range_close: Optional[float] = None
    range_far: Optional[float] = None
    angle: Optional[float] = None
    lose_angle: Optional[float] = None
