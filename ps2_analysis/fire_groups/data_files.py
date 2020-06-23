import json
import os
from typing import Dict, List, Optional

import ndjson
from ps2_census import Query

from .queries import fire_group_query_factory

DATA_FILENAME = "fire-groups.ndjson"

QUERY_BATCH_SIZE: int = 10


def update_data_files(
    service_id: str, directory: str, force_update: bool = False,
):

    filepath: str = "/".join((directory, DATA_FILENAME))
    print(f"Updating {filepath}")

    if os.path.exists(filepath):
        if force_update is True:
            print("Removing previous file")
            os.remove(filepath)
        else:
            print("File already exists")
            return

    total_items: int = 0

    with open(filepath, "a") as f:

        previously_returned: Optional[int] = None

        i: int = 0
        while previously_returned is None or previously_returned > 0:
            query: Query = fire_group_query_factory().set_service_id(service_id).start(
                i
            ).limit(QUERY_BATCH_SIZE)
            result: dict = query.get()

            try:
                returned: int = result["returned"]
            except KeyError:
                print(result)
                raise

            local: int = 0
            for item in result["fire_group_list"]:
                local += 1
                f.write(f"{json.dumps(item)}\n")

            total_items += local
            i += QUERY_BATCH_SIZE

            print(f"Got {local} items, total {total_items}")

            previously_returned = returned

    print(f"Saved {total_items} items")


def load_data_files(directory: str) -> List[Dict]:
    filepath: str = "/".join((directory, DATA_FILENAME))
    with open(filepath) as f:
        data = ndjson.load(f)

    print(f"Loaded {len(data)} items from {filepath}")
    return data
