import os
from typing import Dict, List, Optional

from ps2_analysis.data_file import DataFile, update_data_file
from ps2_analysis.weapons.classes.infantry_weapon import InfantryWeapon
from ps2_analysis.weapons.infantry_weapons import generate_infantry_weapons

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_data_file(
    data_file=DataFile.WEAPONS, directory=DATAFILES_DIRECTORY, service_id=SERVICE_ID
)

infantry_weapons: List[InfantryWeapon] = generate_infantry_weapons(
    data_files_directory=DATAFILES_DIRECTORY
)

item_id_idx: Dict[int, InfantryWeapon] = {w.item_id: w for w in infantry_weapons}
