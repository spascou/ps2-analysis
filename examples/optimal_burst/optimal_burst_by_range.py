import logging
import os
from itertools import groupby
from typing import List, Optional

import altair
from ps2_census.enums import PlayerState

from ps2_analysis.enums import DamageLocation
from ps2_analysis.fire_groups.cone_of_fire import ConeOfFire
from ps2_analysis.fire_groups.data_files import (
    update_data_files as update_fire_groups_data_files,
)
from ps2_analysis.fire_groups.fire_mode import FireMode
from ps2_analysis.utils import CodeTimer
from ps2_analysis.weapons.infantry.data_files import (
    update_data_files as update_infantry_weapons_data_files,
)
from ps2_analysis.weapons.infantry.generate import generate_all_infantry_weapons
from ps2_analysis.weapons.infantry.infantry_weapon import InfantryWeapon

logging.basicConfig(level=logging.INFO)

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "../datafiles"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_fire_groups_data_files(
    directory=DATAFILES_DIRECTORY, service_id=SERVICE_ID,
)

update_infantry_weapons_data_files(
    directory=DATAFILES_DIRECTORY, service_id=SERVICE_ID,
)

infantry_weapons: List[InfantryWeapon] = list(
    generate_all_infantry_weapons(data_files_directory=DATAFILES_DIRECTORY)
)

print(f"Generated {len(infantry_weapons)} infantry weapons")

wp: InfantryWeapon = next(x for x in infantry_weapons if x.item_id == 43)

fm: FireMode = wp.fire_groups[0].fire_modes[1]

cof: ConeOfFire = fm.player_state_cone_of_fire[PlayerState.STANDING]

rttks: List[dict] = []

distance: int
for distance in range(0, 100, 2):

    with CodeTimer(f"determination at {distance}m"):

        burst_length: int
        for burst_length in range(0, int(round(fm.max_consecutive_shots / 4)) + 1, 1):

            control_time: int = cof.recover_time(
                cof.min_cof_angle() + cof.bloom * burst_length
            )

            ttk: int
            timed_out_ratio: float

            ttk, timed_out_ratio = fm.real_time_to_kill(
                distance=distance,
                runs=500,
                control_time=control_time,
                auto_burst_length=burst_length,
                aim_location=DamageLocation.HEAD,
                recoil_compensation=True,
                # recoil_compensation_accuracy=0.1,
            )

            rttks.append(
                {
                    "distance": distance,
                    "control_time": control_time + fm.fire_timing.refire_time,
                    "burst_length": burst_length,
                    "ttk": ttk,
                    "timed_out_ratio": timed_out_ratio,
                }
            )


dataset = altair.Data(values=rttks)

dst_ttk_chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="ttk:Q",
        color=altair.Color("burst_length:O", scale=altair.Scale(scheme="dark2")),
        tooltip=[
            "distance:Q",
            "control_time:Q",
            "burst_length:Q",
            "ttk:Q",
            "timed_out_ratio:Q",
        ],
    )
    .properties(title=f"{wp.name} optimal ttk at distance by burst length", width=900)
    .interactive()
)

dst_tor_chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="timed_out_ratio:Q",
        color=altair.Color("burst_length:O", scale=altair.Scale(scheme="dark2")),
        tooltip=[
            "distance:Q",
            "control_time:Q",
            "burst_length:Q",
            "ttk:Q",
            "timed_out_ratio:Q",
        ],
    )
    .properties(
        title=f"{wp.name} timed out ratio at distance by burst length", width=900
    )
    .interactive()
)


filtered_rttks: List[dict] = []

for _, distance_rttks_it in groupby(
    sorted(rttks, key=lambda x: x["distance"]), lambda x: x["distance"]
):
    distance_rttks: List[dict] = list(distance_rttks_it)

    min_ttk: int = min(
        (x["ttk"] for x in filter(lambda x: x["ttk"] > 0, distance_rttks))
    )

    candidates: List[dict] = list(
        filter(lambda x: 0 <= x["ttk"] <= round(1.05 * min_ttk), distance_rttks)
    )

    auto_candidates: List[dict] = list(
        filter(lambda x: x["burst_length"] == 0, candidates)
    )

    if auto_candidates:

        filtered_rttks.append(min(auto_candidates, key=lambda x: x["ttk"]))

    else:

        filtered_rttks.append(min(candidates, key=lambda x: x["ttk"],))

filtered_dataset = altair.Data(values=filtered_rttks)

burst_length_chart = (
    altair.Chart(filtered_dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="burst_length:Q",
        tooltip=["ttk:Q", "distance:Q", "burst_length:Q", "control_time:Q"],
    )
    .properties(title=f"{wp.name} optimal burst length at distance", width=900)
    .interactive()
)

(dst_ttk_chart & dst_tor_chart & burst_length_chart).save("optimal_burst_by_range.html")
