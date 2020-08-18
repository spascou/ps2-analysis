import logging
import os
from typing import List, Optional

import altair

from ps2_analysis.enums import DamageLocation
from ps2_analysis.fire_groups.data_files import (
    update_data_files as update_fire_groups_data_files,
)
from ps2_analysis.fire_groups.fire_mode import FireMode
from ps2_analysis.weapons.infantry.data_files import (
    update_data_files as update_infantry_weapons_data_files,
)
from ps2_analysis.weapons.infantry.generate import generate_all_infantry_weapons
from ps2_analysis.weapons.infantry.infantry_weapon import InfantryWeapon

logging.basicConfig(level=logging.INFO)

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"

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

distance: int = 50


burst_length: int
for burst_length in range(1, 16, 1):

    control_time: int
    for control_time in range(0, 350, 20):

        ttk: int = fm.real_time_to_kill(
            distance=distance,
            runs=500,
            control_time=control_time,
            auto_burst_length=burst_length,
            aim_location=DamageLocation.HEAD,
            recoil_compensation=True,
            recoil_compensation_accuracy=0.1,
        )

        rttks.append(
            {"control_time": control_time, "burst_length": burst_length, "ttk": ttk}
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
        tooltip=["ttk:Q"],
    )
    .properties(height=900, width=900)
    .interactive()
)

chart.save("optimal_bursting.html")
