import logging
import os
from typing import List, Optional

from ps2_analysis.weapons.vehicle.data_files import update_data_files
from ps2_analysis.weapons.vehicle.generate import generate_all_vehicle_weapons
from ps2_analysis.weapons.vehicle.vehicle_weapon import VehicleWeapon

logging.basicConfig(level=logging.INFO)

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_data_files(
    directory=DATAFILES_DIRECTORY, service_id=SERVICE_ID,
)

vehicle_weapons: List[VehicleWeapon] = list(
    generate_all_vehicle_weapons(data_files_directory=DATAFILES_DIRECTORY)
)

print(f"Generated {len(vehicle_weapons)} vehicle weapons")
