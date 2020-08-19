import logging
import os
import statistics
from itertools import groupby
from typing import List, Optional

import altair

from ps2_analysis.enums import DamageLocation
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

rttks: List[dict] = []

distance: int
for distance in range(0, 100, 5):

    with CodeTimer(f"determination at {distance}m"):

        burst_length: int
        for burst_length in range(1, 11):

            control_time: int
            for control_time in range(
                0, 300, int(round(fm.fire_timing.refire_time / 2))
            ):

                ttk: int
                timed_out_ratio: float

                ttk, timed_out_ratio = fm.real_time_to_kill(
                    distance=distance,
                    runs=200,
                    max_time=3_000,
                    control_time=control_time,
                    auto_burst_length=burst_length,
                    aim_location=DamageLocation.HEAD,
                    recoil_compensation=True,
                )

                rttks.append(
                    {
                        "distance": distance,
                        "control_time": control_time + fm.fire_timing.refire_time,
                        "burst_length": burst_length,
                        "ttk": ttk if timed_out_ratio < 0.20 else -1,
                        "timed_out_ratio": timed_out_ratio,
                    }
                )

filtered_rttks: List[dict] = []

for distance, distance_rttks_it in groupby(
    sorted(rttks, key=lambda x: x["distance"]), lambda x: x["distance"]
):
    els: List[dict] = list(filter(lambda x: x["ttk"] >= 0, distance_rttks_it))

    min_ttk: int = min((x["ttk"] for x in els))
    median_ttk: int = statistics.median((x["ttk"] for x in els))

    if abs(min_ttk - median_ttk) / min_ttk < 0.2:

        filtered_rttks.append(
            {
                "distance": distance,
                "control_time": 0,
                "burst_length": -1,
                "ttk": min_ttk,
                "timed_out_ratio": 0.0,
            }
        )

    else:

        filtered_rttks.append(min(els, key=lambda x: x["ttk"]))

dataset = altair.Data(values=filtered_rttks)

burst_length_chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="burst_length:Q",
        tooltip=["ttk:Q", "distance:Q", "burst_length:Q", "control_time:Q"],
    )
    .properties(title="Optimal burst length at distance", width=900)
    .interactive()
)
control_time_chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="control_time:Q",
        tooltip=["ttk:Q", "distance:Q", "burst_length:Q", "control_time:Q"],
    )
    .properties(title="Optimal control time at distance", width=900)
    .interactive()
)
ttk_chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="ttk:Q",
        tooltip=["ttk:Q", "distance:Q", "burst_length:Q", "control_time:Q"],
    )
    .properties(title="Optimal TTK at distance", width=900)
    .interactive()
)

(burst_length_chart & control_time_chart & ttk_chart).save(
    "optimal_burst_by_range.html"
)
