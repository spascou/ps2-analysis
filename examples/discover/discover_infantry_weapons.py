import json
import os
from typing import Iterator, Optional

from ps2_analysis.fire_groups.data_files import (
    update_data_files as update_fire_groups_data_files,
)
from ps2_analysis.utils import discover
from ps2_analysis.weapons.infantry.data_files import (
    load_data_files as load_infantry_weapons_data_files,
)
from ps2_analysis.weapons.infantry.data_files import (
    update_data_files as update_infantry_weapons_data_files,
)

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

data: Iterator[dict] = load_infantry_weapons_data_files(directory=DATAFILES_DIRECTORY)

print(
    json.dumps(
        {k: sorted(list(v)) for k, v in discover(data).items()},
        sort_keys=True,
        indent=2,
    )
)
