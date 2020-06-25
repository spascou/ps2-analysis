from typing import Callable

from ps2_census import Collection, Join

# Fire group to fire mode
fire_group_to_fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_GROUP_TO_FIRE_MODE)
    .list(1)
    .on("fire_group_id")
    .to("fire_group_id")
    .inject_at("fire_group_to_fire_modes")
    .get_factory()
)

fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_2)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode")
    .get_factory()
)

# Fire mode to direct damage effect
fire_mode_to_damage_direct_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_direct_effect_id")
    .to("effect_id")
    .inject_at("damage_direct_effect")
    .nest(
        Join(Collection.EFFECT_TYPE)
        .on("effect_type_id")
        .to("effect_type_id")
        .inject_at("effect_type")
    )
    .get_factory()
)

# Fire mode to indirect damage effect
fire_mode_to_damage_indirect_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_indirect_effect_id")
    .to("effect_id")
    .inject_at("damage_indirect_effect")
    .nest(
        Join(Collection.EFFECT_TYPE)
        .on("effect_type_id")
        .to("effect_type_id")
        .inject_at("effect_type")
    )
    .get_factory()
)

# Fire mode to ability
fire_mode_to_ability_join_factory: Callable[[], Join] = (
    Join(Collection.ABILITY)
    .on("ability_id")
    .to("ability_id")
    .inject_at("ability")
    .nest(
        Join(Collection.ABILITY_TYPE)
        .on("ability_type_id")
        .to("ability_type_id")
        .inject_at("ability_type")
    )
    .get_factory()
)

# Fire mode to projectile
fire_mode_to_projectile_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_TO_PROJECTILE)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode_to_projectile")
    .get_factory()
)

projectile_join_factory: Callable[[], Join] = (
    Join(Collection.PROJECTILE).inject_at("projectile").get_factory()
)

# Player state group
player_state_group_join_factory: Callable[[], Join] = (
    Join(Collection.PLAYER_STATE_GROUP_2)
    .list(1)
    .on("player_state_group_id")
    .to("player_state_group_id")
    .inject_at("player_state_groups")
    .get_factory()
)
