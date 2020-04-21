import json
import os
from enum import Enum
from typing import Callable, Dict, List, Optional

import ndjson
from ps2_census import Query

from .weapons.queries import full_weapons_query_factory


class DataFile(str, Enum):
    WEAPONS = f"weapons.ndjson"


DATA_FILE_QUERY_FACTORY: Dict[DataFile, Callable[[], Query]] = {
    DataFile.WEAPONS: full_weapons_query_factory
}

DATA_FILE_QUERY_BATCH_SIZE: Dict[DataFile, int] = {DataFile.WEAPONS: 20}


def update_all_data_files(
    service_id: str, directory: str, force_update: bool = False,
):
    print("Updating all data files")

    data_file: DataFile
    for data_file in DATA_FILE_QUERY_FACTORY.keys():
        update_data_file(
            service_id=service_id,
            data_file=data_file,
            directory=directory,
            force_update=force_update,
        )


def update_data_file(
    service_id: str, data_file: DataFile, directory: str, force_update: bool = False,
):
    query_factory: Callable[[], Query] = DATA_FILE_QUERY_FACTORY[data_file]
    query_batch_size: int = DATA_FILE_QUERY_BATCH_SIZE[data_file]

    filepath: str = "/".join((directory, data_file.value))
    print(f"Updating {filepath}")

    if os.path.exists(filepath):
        if force_update is True:
            print(f"Removing previous file")
            os.remove(filepath)
        else:
            print("File already exists")
            return

    total_items: int = 0
    previously_returned: Optional[int] = None

    with open(filepath, "a") as f:
        i: int = 1
        while previously_returned is None or previously_returned > 0:
            query: Query = query_factory().set_service_id(service_id).start(i).limit(
                query_batch_size
            )
            result: dict = query.get()

            try:
                returned: int = result["returned"]
            except KeyError:
                print(result)
                raise

            local: int = 0
            for item in result["item_list"]:
                local += 1
                f.write(f"{json.dumps(item)}\n")

            total_items += local
            i += query_batch_size

            print(f"Got {local} items, total {total_items}")

            previously_returned = returned

    print(f"Saved {total_items} items")


def load_data_file(data_file: DataFile, directory: str) -> List[Dict]:
    filepath: str = "/".join((directory, data_file.value))
    with open(filepath) as f:
        data = ndjson.load(f)

    print(f"Loaded {len(data)} items from {filepath}")
    return data
