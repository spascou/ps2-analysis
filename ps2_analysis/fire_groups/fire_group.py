from dataclasses import dataclass, field
from typing import List

from .fire_mode import FireMode


@dataclass
class FireGroup:
    # General information
    fire_group_id: int
    description: str
    transition_time: int

    # Fire modes
    fire_modes: List[FireMode] = field(default_factory=list)