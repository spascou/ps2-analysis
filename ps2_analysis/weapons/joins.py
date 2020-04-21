from typing import Callable

from ps2_census import Collection, Join

item_to_weapon_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_TO_WEAPON)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .inject_at("item_to_weapon")
    .get_factory()
)

weapon_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON)
    .outer(0)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon")
    .get_factory()
)

weapon_to_fire_group_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_TO_FIRE_GROUP)
    .outer(0)
    .list(1)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon_to_fire_groups")
    .get_factory()
)

fire_group_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_GROUP)
    .outer(0)
    .on("fire_group_id")
    .to("fire_group_id")
    .inject_at("fire_group")
    .get_factory()
)

fire_group_to_fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_GROUP_TO_FIRE_MODE)
    .outer(0)
    .list(1)
    .on("fire_group_id")
    .to("fire_group_id")
    .inject_at("fire_group_to_fire_modes")
    .get_factory()
)

fire_mode_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_2)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode")
    .get_factory()
)

fire_mode_to_direct_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_direct_effect_id")
    .to("effect_id")
    .inject_at("direct_effect")
    .get_factory()
)

fire_mode_to_indirect_effect_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT)
    .on("damage_indirect_effect_id")
    .to("effect_id")
    .inject_at("indirect_effect")
    .get_factory()
)

effect_to_effect_type_join_factory: Callable[[], Join] = (
    Join(Collection.EFFECT_TYPE)
    .outer(0)
    .on("effect_type_id")
    .to("effect_type_id")
    .inject_at("effect_type")
    .get_factory()
)

fire_mode_to_projectile_join_factory: Callable[[], Join] = (
    Join(Collection.FIRE_MODE_TO_PROJECTILE)
    .outer(0)
    .on("fire_mode_id")
    .to("fire_mode_id")
    .inject_at("fire_mode_to_projectile")
    .get_factory()
)

projectile_join_factory: Callable[[], Join] = (
    Join(Collection.PROJECTILE).outer(0).inject_at("projectile").get_factory()
)

player_state_group_join_factory: Callable[[], Join] = (
    Join(Collection.PLAYER_STATE_GROUP_2)
    .outer(0)
    .list(1)
    .on("player_state_group_id")
    .to("player_state_group_id")
    .inject_at("player_state_groups")
    .get_factory()
)

item_attachment_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_ATTACHMENT)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .list(1)
    .inject_at("item_attachments")
    .nest(
        Join(Collection.ITEM)
        .outer(0)
        .on("attachment_item_id")
        .to("item_id")
        .inject_at("item")
        .nest(
            Join(Collection.ZONE_EFFECT)
            .outer(0)
            .on("passive_ability_id")
            .to("ability_id")
            .list(1)
            .inject_at("zone_effects")
            .nest(
                Join(Collection.ZONE_EFFECT_TYPE)
                .outer(0)
                .on("zone_effect_type_id")
                .to("zone_effect_type_id")
                .inject_at("zone_effect_type")
            )
        )
    )
    .get_factory()
)

weapon_datasheet_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_DATASHEET)
    .outer(0)
    .on("item_id")
    .to("item_id")
    .inject_at("weapon_datasheet")
    .get_factory()
)
