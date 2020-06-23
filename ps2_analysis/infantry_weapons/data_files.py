import json
import os
from typing import Callable, Dict, List, Optional, Set

import ndjson
from ps2_census import Query
from ps2_census.enums import ItemCategory, ItemType

from .queries import infantry_weapons_query_factory

DATA_FILENAME = "infantry-weapons.ndjson"


QUERY_FACTORY: Callable[[], Query] = infantry_weapons_query_factory

QUERY_BATCH_SIZE: int = 10

ITEM_CATEGORIES: Set[ItemCategory] = {
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
    ItemCategory.AERIAL_COMBAT_WEAPON,
}

ITEM_TYPE: ItemType = ItemType.WEAPON


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

        item_category: ItemCategory
        for item_category in ITEM_CATEGORIES:
            print(f"For category {item_category.name}")

            previously_returned: Optional[int] = None

            i: int = 0
            while previously_returned is None or previously_returned > 0:
                query: Query = QUERY_FACTORY().set_service_id(service_id).filter(
                    "item_type_id", ITEM_TYPE.value
                ).filter("item_category_id", item_category.value).start(i).limit(
                    QUERY_BATCH_SIZE
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
