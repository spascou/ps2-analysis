from dataclasses import dataclass, field
from typing import List, Optional

from .fire_mode import FireMode
from .fire_timing import FireTiming


@dataclass
class FireGroup:
    fire_group_id: int
    description: str
    transition_time: int
    fire_modes: List[FireMode] = field(default_factory=list)

    @property
    def fire_timing(self) -> Optional[FireTiming]:
        pass
