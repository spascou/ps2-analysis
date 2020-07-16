from enum import Enum


class DamageLocation(str, Enum):
    HEAD = "head"
    LEGS = "legs"
    TORSO = "torso"


class DamageTargetType(str, Enum):
    INFANTRY_BASELINE = "infantry_baseline"
    INFANTRY_AUXILIARY_SHIELD = "infantry_auxiliary_shield"
    INFANTRY_INFILTRATOR = "infantry_infiltrator"
    INFANTRY_HEAVY_RESIST_SHIELD = "infantry_heavy_resist_shield"
    INFANTRY_HEAVY_HEALTH_SHIELD = "infantry_heavy_health_shield"
    INFANTRY_NANOWEAVE = "infantry_nanoweave"
    INFANTRY_FLAK_ARMOR = "infantry_flak_armor"
