from typing import Any, Dict

from ps2_census.enums import ResistType

from .enums import DamageLocation, DamageTargetType

DAMAGE_TARGET_TYPE_DATA: Dict[DamageTargetType, Dict[str, Any]] = {
    DamageTargetType.INFANTRY_BASELINE: {"health": 500, "shields": 500},
    DamageTargetType.INFANTRY_AUXILIARY_SHIELD: {"health": 500, "shields": 550},
    DamageTargetType.INFANTRY_INFILTRATOR: {"health": 400, "shields": 500},
    DamageTargetType.INFANTRY_HEAVY_RESIST_SHIELD: {
        "health": 500,
        "shields": 500,
        "damage_resistance": {"any": {"any": 0.35}},
    },
    DamageTargetType.INFANTRY_HEAVY_HEALTH_SHIELD: {
        "health": 500 + 450,
        "shields": 500,
    },
    DamageTargetType.INFANTRY_NANOWEAVE: {
        "health": 500,
        "shields": 500,
        "damage_resistance": {
            frozenset({DamageLocation.TORSO, DamageLocation.LEGS}): {
                frozenset(
                    {
                        ResistType.SMALL_ARM,
                        ResistType.HEAVY_MACHINE_GUN,
                        ResistType.ARMOR_PIERCING_CHAIN_GUN,
                        ResistType.AIRCRAFT_MACHINE_GUN,
                        ResistType.ANTI_AIRCRAFT_MACHINE_GUN,
                        ResistType.ANTI_MATERIEL_RIFLE,
                    }
                ): 0.2
            }
        },
    },
    DamageTargetType.INFANTRY_FLAK_ARMOR: {
        "health": 500,
        "shields": 500,
        "damage_resistance": {
            "any": {
                frozenset({ResistType.EXPLOSIVE, ResistType.ANTI_VEHICLE_MINE}): 0.5,
                frozenset(
                    {
                        ResistType.DEFAULT_ROCKET_LAUNCHER,
                        ResistType.ARMOR_PIERCING_CHAIN_GUN,
                        ResistType.AIR_TO_GROUND_WARHEAD,
                    }
                ): 0.2,
            }
        },
    },
}
