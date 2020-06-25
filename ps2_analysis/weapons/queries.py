from typing import Callable

from ps2_census import Collection, Query

from .joins import (
    item_attachment_join_factory,
    item_to_weapon_join_factory,
    weapon_datasheet_join_factory,
    weapon_join_factory,
    weapon_to_fire_group_join_factory,
)

weapon_query_factory: Callable[[], Query] = (
    Query(Collection.ITEM)
    .lang("en")
    .sort(("item_id", 1))
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(weapon_to_fire_group_join_factory())
        )
    )
    .join(item_attachment_join_factory())
    .join(weapon_datasheet_join_factory())
    .get_factory()
)
