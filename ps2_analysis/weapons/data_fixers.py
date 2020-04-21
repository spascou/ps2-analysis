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
}
