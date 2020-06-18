import json
import logging
import os
from typing import Dict, List, Optional

from ps2_analysis.data_file import DataFile, update_data_file
from ps2_analysis.vehicle_weapons.generate import generate_vehicle_weapons
from ps2_analysis.vehicle_weapons.vehicle_weapon import VehicleWeapon

logging.basicConfig(level=logging.INFO)

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_data_file(
    data_file=DataFile.VEHICLE_WEAPONS,
    directory=DATAFILES_DIRECTORY,
    service_id=SERVICE_ID,
)

vehicle_weapons: List[VehicleWeapon] = generate_vehicle_weapons(
    data_files_directory=DATAFILES_DIRECTORY
)

item_id_idx: Dict[int, VehicleWeapon] = {w.item_id: w for w in vehicle_weapons}

# print(
#     json.dumps(
#         {i.name: i.category.name for i in vehicle_weapons}, sort_keys=True, indent=2
#     )
# )