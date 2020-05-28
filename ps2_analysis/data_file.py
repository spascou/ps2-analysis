import json
import os
from enum import Enum
from typing import Callable, Dict, List, Optional, Set

import ndjson
from ps2_census import Query
from ps2_census.enums import ItemCategory, ItemType

from .infantry_weapons.queries import infantry_weapons_query_factory


class DataFile(str, Enum):
    INFANTRY_WEAPONS = "infantry-weapons.ndjson"


DATA_FILE_QUERY_FACTORY: Dict[DataFile, Callable[[], Query]] = {
    DataFile.INFANTRY_WEAPONS: infantry_weapons_query_factory
}

DATA_FILE_QUERY_BATCH_SIZE: Dict[DataFile, int] = {DataFile.INFANTRY_WEAPONS: 10}

DATA_FILE_ITEM_CATEGORIES: Dict[DataFile, Set[ItemCategory]] = {
    DataFile.INFANTRY_WEAPONS: {
        ItemCategory.EXPLOSIVE,
        ItemCategory.GRENADE,
        ItemCategory.ROCKET_LAUNCHER,
        ItemCategory.KNIFE,
        ItemCategory.PISTOL,
        ItemCategory.SHOTGUN,
        ItemCategory.SMG,
        ItemCategory.LMG,
        ItemCategory.ASSAULT_RIFLE,
        ItemCategory.CARBINE,
        ItemCategory.SNIPER_RIFLE,
        ItemCategory.SCOUT_RIFLE,
        ItemCategory.HEAVY_WEAPON,
        ItemCategory.BATTLE_RIFLE,
        ItemCategory.CROSSBOW,
        ItemCategory.HYBRID_RIFLE,
    }
}

DATA_FILE_ITEM_TYPE: Dict[DataFile, ItemType] = {
    DataFile.INFANTRY_WEAPONS: ItemType.WEAPON
}


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
    item_type: ItemType = DATA_FILE_ITEM_TYPE[data_file]
    item_categories: Set[ItemCategory] = DATA_FILE_ITEM_CATEGORIES[data_file]

    filepath: str = "/".join((directory, data_file.value))
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

        item_category: ItemCategory
        for item_category in item_categories:
            print(f"For category {item_category.name}")

            previously_returned: Optional[int] = None

            i: int = 0
            while previously_returned is None or previously_returned > 0:
                query: Query = query_factory().set_service_id(service_id).filter(
                    "item_type_id", item_type.value
                ).filter("item_category_id", item_category.value).start(i).limit(
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
