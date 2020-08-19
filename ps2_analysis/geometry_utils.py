import functools
import math
import random
from typing import Optional, Tuple

from ps2_analysis.fire_groups.damage_profile import DamageLocation

from .utils import fastround


@functools.lru_cache
def planetman_hit_location(
    x: float,
    y: float,
    aim_location: DamageLocation = DamageLocation.TORSO,
    # Planetman dimensions, as three stacked rectangles, in meters
    # Total planetman height: 1.80m
    width: float = 0.35,
    head_height: float = 0.25,
    torso_height: float = 0.60,
    legs_height: float = 0.95,
) -> Optional[DamageLocation]:

    hit_location: Optional[DamageLocation] = None

    half_width: float = width / 2
    half_head_height: float = head_height / 2
    half_torso_height: float = torso_height / 2
    half_legs_height: float = legs_height / 2

    head_y_delta: float = 0.0
    torso_y_delta: float = 0.0
    legs_y_delta: float = 0.0

    if aim_location == DamageLocation.HEAD:

        torso_y_delta -= half_head_height + half_torso_height
        legs_y_delta -= half_head_height + torso_height + half_legs_height

    elif aim_location == DamageLocation.TORSO:

        head_y_delta += half_torso_height + half_head_height
        legs_y_delta -= half_torso_height + half_legs_height

    elif aim_location == DamageLocation.LEGS:

        head_y_delta += half_legs_height + torso_height + half_head_height
        torso_y_delta += half_head_height + half_torso_height

    else:

        raise ValueError(f"Unsupported aim location: {aim_location}")

    if -half_width <= x <= half_width:

        if head_y_delta - half_head_height <= y <= head_y_delta + half_head_height:

            hit_location = DamageLocation.HEAD

        elif (
            torso_y_delta - half_torso_height <= y <= torso_y_delta + half_torso_height
        ):

            hit_location = DamageLocation.TORSO

        elif legs_y_delta - half_legs_height <= y <= legs_y_delta + half_legs_height:

            hit_location = DamageLocation.LEGS

    return hit_location


def random_point_in_disk(
    radius: float, precision_decimals: int = 6
) -> Tuple[float, float]:

    srandom = random.SystemRandom()

    cof_h: float = radius
    cof_v: float = radius

    while math.sqrt(cof_h ** 2 + cof_v ** 2) > radius:

        cof_h = fastround(srandom.uniform(-radius, radius), precision_decimals)
        cof_v = fastround(srandom.uniform(-radius, radius), precision_decimals)

    return (cof_h, cof_v)
