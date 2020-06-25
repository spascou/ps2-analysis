import json
import os
from typing import Dict, List, Optional, Set

import ndjson
from ps2_census import Query
from ps2_census.enums import ItemCategory, ItemType

from ps2_analysis.weapons.queries import weapon_query_factory

DATA_FILENAME = "vehicle-weapons.ndjson"

QUERY_BATCH_SIZE: int = 50

ITEM_CATEGORIES: Set[ItemCategory] = {
    ItemCategory.VEHICLE_WEAPONS,
    ItemCategory.FLASH_PRIMARY_WEAPON,
    ItemCategory.GALAXY_LEFT_WEAPON,
    ItemCategory.GALAXY_TAIL_WEAPON,
    ItemCategory.GALAXY_RIGHT_WEAPON,
    ItemCategory.GALAXY_TOP_WEAPON,
    ItemCategory.HARASSER_TOP_GUNNER,
    ItemCategory.LIBERATOR_BELLY_WEAPON,
    ItemCategory.LIBERATOR_NOSE_CANNON,
    ItemCategory.LIBERATOR_TAIL_WEAPON,
    ItemCategory.LIGHTNING_PRIMARY_WEAPON,
    ItemCategory.MAGRIDER_GUNNER_WEAPON,
    ItemCategory.MAGRIDER_PRIMARY_WEAPON,
    ItemCategory.MOSQUITO_NOSE_CANNON,
    ItemCategory.MOSQUITO_WING_MOUNT,
    ItemCategory.PROWLER_GUNNER_WEAPON,
    ItemCategory.PROWLER_PRIMARY_WEAPON,
    ItemCategory.REAVER_NOSE_CANNON,
    ItemCategory.REAVER_WING_MOUNT,
    ItemCategory.SCYTHE_NOSE_CANNON,
    ItemCategory.SCYTHE_WING_MOUNT,
    ItemCategory.SUNDERER_FRONT_GUNNER,
    ItemCategory.SUNDERER_REAR_GUNNER,
    ItemCategory.VANGUARD_GUNNER_WEAPON,
    ItemCategory.VANGUARD_PRIMARY_WEAPON,
    ItemCategory.VALKYRIE_NOSE_GUNNER,
    ItemCategory.ANT_TOP_TURRET,
    ItemCategory.BASTION_POINT_DEFENSE,
    ItemCategory.BASTION_BOMBARD,
    ItemCategory.BASTION_WEAPON_SYSTEM,
    ItemCategory.COLOSSUS_PRIMARY_WEAPON,
    ItemCategory.COLOSSUS_FRONT_RIGHT_WEAPON,
    ItemCategory.COLOSSUS_FRONT_LEFT_WEAPON,
    ItemCategory.COLOSSUS_REAR_RIGHT_WEAPON,
    ItemCategory.COLOSSUS_REAR_LEFT_WEAPON,
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
                query: Query = weapon_query_factory().set_service_id(service_id).filter(
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
