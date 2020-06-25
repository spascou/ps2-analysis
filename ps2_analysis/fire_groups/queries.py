from typing import Callable

from ps2_census import Collection, Query

from .joins import (
    fire_group_to_fire_mode_join_factory,
    fire_mode_join_factory,
    fire_mode_to_ability_join_factory,
    fire_mode_to_damage_direct_effect_join_factory,
    fire_mode_to_damage_indirect_effect_join_factory,
    fire_mode_to_projectile_join_factory,
    player_state_group_join_factory,
    projectile_join_factory,
)

fire_group_query_factory: Callable[[], Query] = (
    Query(Collection.FIRE_GROUP)
    .lang("en")
    .sort(("fire_group_id", 1))
    .join(
        fire_group_to_fire_mode_join_factory().nest(
            fire_mode_join_factory().nest(player_state_group_join_factory())
        )
    )
    .join(
        fire_group_to_fire_mode_join_factory().nest(
            fire_mode_join_factory().nest(
                fire_mode_to_damage_direct_effect_join_factory()
            )
        )
    )
    .join(
        fire_group_to_fire_mode_join_factory().nest(
            fire_mode_join_factory().nest(
                fire_mode_to_damage_indirect_effect_join_factory()
            )
        )
    )
    .join(
        fire_group_to_fire_mode_join_factory().nest(
            fire_mode_join_factory().nest(fire_mode_to_ability_join_factory())
        )
    )
    .join(
        fire_group_to_fire_mode_join_factory().nest(
            fire_mode_join_factory().nest(
                fire_mode_to_projectile_join_factory().nest(projectile_join_factory())
            )
        )
    )
    .get_factory()
)
