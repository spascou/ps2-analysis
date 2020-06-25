from typing import Callable, Dict


def serpent_ve92_first_fire_group(data: dict):
    data["fire_group_to_fire_modes"][1]["fire_mode"]["description"]["en"] = "Auto"


def serpent_ve92_second_fire_group(data: dict):
    data["fire_group_to_fire_modes"][1]["fire_mode"]["description"]["en"] = "Semi-Auto"


def nc05_jackhammer_second_fire_group(data: dict):
    data["fire_group_to_fire_modes"][0]["fire_mode"]["fire_mode_type_id"] = "0"


def ns_11_second_fire_group(data: dict):
    data["fire_group_to_fire_modes"][0]["fire_mode"]["fire_mode_type_id"] = "0"


def beamer_vs3_first_fire_group(data: dict):
    psg: dict = data["fire_group_to_fire_modes"][1]["fire_mode"]["player_state_groups"][
        4
    ]

    psg["cof_min"], psg["cof_max"] = psg["cof_max"], psg["cof_min"]


FIRE_GROUP_DATA_FIXERS: Dict[int, Callable[[dict], None]] = {
    7214: serpent_ve92_first_fire_group,
    1022: serpent_ve92_second_fire_group,
    94: nc05_jackhammer_second_fire_group,
    80103: nc05_jackhammer_second_fire_group,
    80332: nc05_jackhammer_second_fire_group,
    21501: ns_11_second_fire_group,
    70015: ns_11_second_fire_group,
    80592: ns_11_second_fire_group,
    11: beamer_vs3_first_fire_group,
    766: beamer_vs3_first_fire_group,
    7403: beamer_vs3_first_fire_group,
}
