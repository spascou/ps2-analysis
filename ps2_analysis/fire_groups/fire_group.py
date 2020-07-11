from dataclasses import dataclass, field
from typing import List

from .fire_mode import FireMode


@dataclass
class FireGroup:
    fire_group_id: int
    description: str
    transition_time: int
    fire_modes: List[FireMode] = field(default_factory=list)
