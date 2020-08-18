import logging
import os
from typing import List, Optional, Tuple

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

sim = fm.simulate_shots(
    shots=fm.max_consecutive_shots,
    recoil_compensation=True,
    recoil_compensation_accuracy=0.1,
)

datapoints: List[dict] = []

t: int
cursor_coor: Tuple[float, float]
pellets_coors: List[Tuple[float, float]]
_cof: float
_vertical_recoil: Tuple[float, float]
_horizontal_recoil: Tuple[float, float]
for t, cursor_coor, pellets_coors, _cof, _vertical_recoil, _horizontal_recoil in sim:
    cursor_x, cursor_y = cursor_coor

    datapoints.append({"time": t, "type": "cursor", "x": cursor_x, "y": cursor_y})

    for pellet_x, pellet_y in pellets_coors:
        datapoints.append({"time": t, "type": "pellet", "x": pellet_x, "y": pellet_y})


dataset = altair.Data(values=datapoints)

chart = (
    altair.Chart(dataset)
    .mark_point()
    .encode(
        x="x:Q",
        y="y:Q",
        color=altair.Color("type:O", scale=altair.Scale(scheme="dark2")),
        tooltip=["time:Q", "x:Q", "y:Q"],
    )
    .properties(height=900, width=900)
    .interactive()
)

chart.save("shooting_simulation_compensated.html")
