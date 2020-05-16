from typing import Callable, Dict


def nc05_jackhammer(data: dict):
    data["item_to_weapon"]["weapon"]["weapon_to_fire_groups"][1]["fire_group"][
        "fire_group_to_fire_modes"
    ][0]["fire_mode"]["fire_mode_type_id"] = "0"


def ns_11(data: dict):
    data["item_to_weapon"]["weapon"]["weapon_to_fire_groups"][1]["fire_group"][
        "fire_group_to_fire_modes"
    ][0]["fire_mode"]["fire_mode_type_id"] = "0"


def beamer_vs3(data: dict):
    psg: dict = data["item_to_weapon"]["weapon"]["weapon_to_fire_groups"][0][
        "fire_group"
    ]["fire_group_to_fire_modes"][1]["fire_mode"]["player_state_groups"][4]

    psg["cof_min"], psg["cof_max"] = psg["cof_max"], psg["cof_min"]


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


def serpent_ve92(data: dict):
    data["item_to_weapon"]["weapon"]["weapon_to_fire_groups"][0]["fire_group"][
        "fire_group_to_fire_modes"
    ][1]["fire_mode"]["description"]["en"] = "Auto"
    data["item_to_weapon"]["weapon"]["weapon_to_fire_groups"][1]["fire_group"][
        "fire_group_to_fire_modes"
    ][1]["fire_mode"]["description"]["en"] = "Semi-Auto"


INFANTRY_WEAPONS_DATA_FIXERS: Dict[int, Callable[[dict], None]] = {
    7528: nc05_jackhammer,
    803756: nc05_jackhammer,
    6004174: nc05_jackhammer,
    69999: ns_11,
    70998: ns_11,
    75005: ns_11,
    75234: ns_11,
    802099: ns_11,
    802100: ns_11,
    802101: ns_11,
    802102: ns_11,
    6003571: ns_11,
    6008371: ns_11,
    21: beamer_vs3,
    1959: beamer_vs3,
    7403: beamer_vs3,
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
    7214: serpent_ve92,
}
