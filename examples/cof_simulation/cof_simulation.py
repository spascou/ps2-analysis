import logging
import os
from typing import List, Optional

import altair

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

datapoints: List[dict] = []

auto_sim = fm.simulate_shots(shots=fm.max_consecutive_shots)

for (
    t,
    _cursor_coor,
    _pellets_coors,
    cof,
    _vertical_recoil,
    _horizontal_recoil,
) in auto_sim:
    datapoints.append({"time": t, "control": "full auto", "cof": cof})

burst_sim = fm.simulate_shots(
    shots=fm.max_consecutive_shots, auto_burst_length=5, control_time=5,
)

for (
    t,
    _cursor_coor,
    _pellets_coors,
    cof,
    _vertical_recoil,
    _horizontal_recoil,
) in burst_sim:
    datapoints.append(
        {
            "time": t,
            "control": f"5 burst + {fm.fire_timing.refire_time + 5}ms",
            "cof": cof,
        }
    )


dataset = altair.Data(values=datapoints)

chart = (
    altair.Chart(dataset)
    .mark_line()
    .encode(
        x="time:Q",
        y="cof:Q",
        color=altair.Color("control:O", scale=altair.Scale(scheme="dark2")),
        tooltip=["time:Q", "control:O"],
    )
    .properties(title="Cone of Fire", height=900, width=900)
    .interactive()
)

chart.save("cof_simulation.html")
