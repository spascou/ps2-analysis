from typing import List

from .fire_mode import FireMode


class FireGroup:
    # General information
    index: int
    transition_time: int

    # Fire modes
    fire_modes: List[FireMode]

    def __init__(
        self,
        # General information
        index: int,
        transition_time: int,
    ):
        # General information
        self.index = index
        self.transition_time = transition_time

        # Fire modes
        self.fire_modes = []
