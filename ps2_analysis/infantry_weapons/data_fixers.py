from typing import Callable, Dict


def betelgeuse_54_a(data: dict):
    del data["weapon_datasheet"]["capacity"]
    del data["weapon_datasheet"]["clip_size"]


def darkstar(data: dict):
    del data["weapon_datasheet"]["capacity"]
    del data["weapon_datasheet"]["clip_size"]


def eclipse_ve3a(data: dict):
    del data["weapon_datasheet"]["capacity"]
    del data["weapon_datasheet"]["clip_size"]


def patriot_flare_gun(data: dict):
    data["weapon_datasheet"] = {"capacity": "22", "clip_size": "2"}


def ns_deep_freeze(data: dict):
    data["weapon_datasheet"] = {"capacity": "22", "clip_size": "2"}


def ns_candycannon(data: dict):
    data["weapon_datasheet"] = {"capacity": "27", "clip_size": "3"}


def ns_blackhand(data: dict):
    data["weapon_datasheet"] = {"capacity": "36", "clip_size": "4"}


def ns_showdown(data: dict):
    data["weapon_datasheet"] = {"capacity": "32", "clip_size": "4"}


def triumph_flare_gun(data: dict):
    data["weapon_datasheet"] = {"capacity": "22", "clip_size": "2"}


INFANTRY_WEAPONS_DATA_FIXERS: Dict[int, Callable[[dict], None]] = {
    1894: betelgeuse_54_a,
    1909: darkstar,
    1919: eclipse_ve3a,
    75490: patriot_flare_gun,
    75517: patriot_flare_gun,
    75519: patriot_flare_gun,
    75521: patriot_flare_gun,
    76358: ns_deep_freeze,
    801970: ns_candycannon,
    802733: ns_blackhand,
    802782: ns_blackhand,
    804960: ns_blackhand,
    6002661: ns_blackhand,
    803007: triumph_flare_gun,
    803008: triumph_flare_gun,
    803009: triumph_flare_gun,
    6003793: ns_showdown,
}


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
