from typing import Callable

from ps2_census import Collection, Query

from .joins import (
    fire_group_join_factory,
    fire_group_to_fire_mode_join_factory,
    fire_mode_join_factory,
    fire_mode_to_damage_direct_effect_join_factory,
    fire_mode_to_damage_indirect_effect_join_factory,
    fire_mode_to_projectile_join_factory,
    item_attachment_join_factory,
    item_to_weapon_join_factory,
    player_state_group_join_factory,
    projectile_join_factory,
    weapon_datasheet_join_factory,
    weapon_join_factory,
    weapon_to_fire_group_join_factory,
)

vehicle_weapons_query_factory: Callable[[], Query] = (
    Query(Collection.ITEM)
    .lang("en")
    .sort(("item_id", 1))
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                player_state_group_join_factory()
                            )
                        )
                    )
                )
            )
        )
    )
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                fire_mode_to_damage_direct_effect_join_factory()
                            )
                        )
                    )
                )
            )
        )
    )
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                fire_mode_to_damage_indirect_effect_join_factory()
                            )
                        )
                    )
                )
            )
        )
    )
    .join(
        item_to_weapon_join_factory().nest(
            weapon_join_factory().nest(
                weapon_to_fire_group_join_factory().nest(
                    fire_group_join_factory().nest(
                        fire_group_to_fire_mode_join_factory().nest(
                            fire_mode_join_factory().nest(
                                fire_mode_to_projectile_join_factory().nest(
                                    projectile_join_factory()
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    .join(item_attachment_join_factory())
    .join(weapon_datasheet_join_factory())
    .get_factory()
)