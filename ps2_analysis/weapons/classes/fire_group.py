from .fire_mode import FireMode


class FireGroup:
    # General information
    index: int
    transition_time: int

    # Fire modes
    hip_fire_mode: FireMode
    ads_fire_mode: FireMode

    def __init__(
        self,
        # General information
        index: int,
        transition_time: int,
        # Fire modes
        hip_fire_mode: FireMode,
        ads_fire_mode: FireMode,
    ):
        # General information
        self.index = index
        self.transition_time = transition_time

        # Fire modes
        self.hip_fire_mode = hip_fire_mode
        self.ads_fire_mode = ads_fire_mode
