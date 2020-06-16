import json
import os
from typing import List, Optional

from ps2_analysis.data_file import DataFile, load_data_file, update_data_file
from ps2_analysis.utils import discover

SERVICE_ID: Optional[str] = os.environ.get("CENSUS_SERVICE_ID")
DATAFILES_DIRECTORY: str = "datafiles"

if not SERVICE_ID:
    raise ValueError("CENSUS_SERVICE_ID envvar not found")

update_data_file(
    data_file=DataFile.INFANTRY_WEAPONS,
    directory=DATAFILES_DIRECTORY,
    service_id=SERVICE_ID,
)

data: List[dict] = load_data_file(
    data_file=DataFile.INFANTRY_WEAPONS, directory=DATAFILES_DIRECTORY
)

print(
    json.dumps(
        {k: sorted(list(v)) for k, v in discover(data).items()},
        sort_keys=True,
        indent=2,
    )
)
