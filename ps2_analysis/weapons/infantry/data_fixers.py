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
