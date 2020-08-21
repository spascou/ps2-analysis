import logging
import os
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

distance: int = 30

burst_length: int
for burst_length in range(0, int(round(fm.max_consecutive_shots / 4)) + 1, 1):

    control_time: int
    for control_time in range(
        0, cof.recover_time(cof.min_cof_angle() + cof.bloom * burst_length * 2) + 10, 10
    ):

        with CodeTimer(
            f"{burst_length} length and {control_time}ms control time simulation"
        ):

            ttk: int
            timed_out_ratio: float

            ttk, timed_out_ratio = fm.real_time_to_kill(
                distance=distance,
                runs=500,
                control_time=control_time,
                auto_burst_length=burst_length,
                aim_location=DamageLocation.TORSO,
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

dataset = altair.Data(values=rttks)

chart = (
    altair.Chart(dataset)
    .mark_rect()
    .encode(
        x="burst_length:O",
        y=altair.Y(
            "control_time:O",
            sort=altair.EncodingSortField("control_time", order="descending"),
        ),
        color=altair.Color(
            "ttk:Q", scale=altair.Scale(scheme="plasma"), sort="descending"
        ),
        tooltip=["ttk:Q", "timed_out_ratio:Q"],
    )
    .properties(
        title=f"{wp.name} TTK by burst length and control time at {distance}m",
        height=900,
        width=900,
    )
    .interactive()
)

chart.save("bursts_ttk_simulation.html")
