import logging
import os
from typing import Dict, List, Optional

import altair

from ps2_analysis.fire_groups.data_files import (
    update_data_files as update_fire_groups_data_files,
)
from ps2_analysis.weapons.infantry.data_files import (
    update_data_files as update_infantry_weapons_data_files,
)
from ps2_analysis.weapons.infantry.generate import generate_infantry_weapons
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

infantry_weapons: List[InfantryWeapon] = generate_infantry_weapons(
    data_files_directory=DATAFILES_DIRECTORY
)

item_id_idx: Dict[int, InfantryWeapon] = {w.item_id: w for w in infantry_weapons}

weapon: Optional[InfantryWeapon] = item_id_idx.get(7256)

if weapon:
    simulation_chart: altair.HConcatChart = weapon.fire_groups[0].fire_modes[
        1
    ].generate_altair_simulation(shots=20, runs=100)

    simulation_chart.save(f"{weapon.slug}_simulation.html")