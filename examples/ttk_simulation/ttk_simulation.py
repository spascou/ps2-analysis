import logging
import os
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

distance_range: List[int] = list(range(0, 60, 2))

rttks: List[dict] = []

distance: int
for distance in distance_range:

    with CodeTimer(f"simulation for distance {distance}"):
        auto_ttk, auto_timeout_ratio = fm.real_time_to_kill(
            distance=distance,
            runs=750,
            recoil_compensation=True,
            aim_location=DamageLocation.HEAD,
        )

        burst_5_20_ttk, burst_5_20_timeout_ratio = fm.real_time_to_kill(
            distance=distance,
            runs=750,
            control_time=10,
            auto_burst_length=5,
            recoil_compensation=True,
            aim_location=DamageLocation.HEAD,
        )

        if auto_timeout_ratio < 0.2:
            rttks.append(
                {"distance": distance, "control": "full auto", "ttk": auto_ttk}
            )

        if burst_5_20_timeout_ratio < 0.2:
            rttks.append(
                {
                    "distance": distance,
                    "control": f"3 burst + {fm.fire_timing.refire_time + 20}ms",
                    "ttk": burst_5_20_ttk,
                }
            )

dataset = altair.Data(values=rttks)

chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="distance:Q",
        y="ttk:Q",
        color=altair.Color("control:O", scale=altair.Scale(scheme="dark2")),
        tooltip=["control:O"],
    )
    .properties(title="TTK by range", height=900, width=900)
    .interactive()
)

chart.save("ttk_simulation.html")
