from enum import Enum


class DamageLocation(str, Enum):
    HEAD = "head"
    LEGS = "legs"
    TORSO = "torso"
