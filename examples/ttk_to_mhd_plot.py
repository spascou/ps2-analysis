import os
from typing import List, Optional

from ps2_census.enums import ItemCategory

from ps2_analysis.data_file import DataFile, update_data_file
from ps2_analysis.visualizations.ttk_to_mhd import (
    generate_infantry_weapons_ttk_to_mhd_plot,
)
from ps2_analysis.weapons.classes.infantry_weapon import InfantryWeapon
from ps2_analysis.weapons.infantry_weapons import generate_infantry_weapons

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"
PLOTS_DIRECTORY: str = "plots"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_data_file(
    data_file=DataFile.WEAPONS, directory=DATAFILES_DIRECTORY, service_id=SERVICE_ID
)

infantry_weapons: List[InfantryWeapon] = generate_infantry_weapons(
    data_files_directory=DATAFILES_DIRECTORY
)

generate_infantry_weapons_ttk_to_mhd_plot(
    weapons=infantry_weapons,
    distance=15,
    categories=[ItemCategory.SMG],
    directory=PLOTS_DIRECTORY,
)
