from typing import List, Optional

from .fire_mode import FireMode


class FireGroup:
    # General information
    index: int
    description: str
    transition_time: int

    # Fire modes
    fire_modes: List[FireMode]

    def __init__(
        self,
        # General information
        index: int,
        description: str,
        transition_time: int,
        # Fire modes
        fire_modes: Optional[List[FireMode]] = None,
    ):
        # General information
        self.index = index
        self.description = description
        self.transition_time = transition_time

        # Fire modes
        self.fire_modes = fire_modes or []
