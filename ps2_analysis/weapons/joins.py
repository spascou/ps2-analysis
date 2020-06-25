from typing import Callable

from ps2_census import Collection, Join

# Item to weapon
item_to_weapon_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_TO_WEAPON)
    .on("item_id")
    .to("item_id")
    .inject_at("item_to_weapon")
    .get_factory()
)

weapon_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon")
    .get_factory()
)

# Weapon to fire groups
weapon_to_fire_group_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_TO_FIRE_GROUP)
    .list(1)
    .on("weapon_id")
    .to("weapon_id")
    .inject_at("weapon_to_fire_groups")
    .get_factory()
)

# Item to attachments
item_attachment_join_factory: Callable[[], Join] = (
    Join(Collection.ITEM_ATTACHMENT)
    .on("item_id")
    .to("item_id")
    .list(1)
    .inject_at("item_attachments")
    .nest(
        Join(Collection.ITEM)
        .on("attachment_item_id")
        .to("item_id")
        .inject_at("item")
        .nest(
            Join(Collection.ZONE_EFFECT)
            .on("passive_ability_id")
            .to("ability_id")
            .list(1)
            .inject_at("zone_effects")
            .nest(
                Join(Collection.ZONE_EFFECT_TYPE)
                .on("zone_effect_type_id")
                .to("zone_effect_type_id")
                .inject_at("zone_effect_type")
            )
        )
    )
    .get_factory()
)

# Weapon to datasheet
weapon_datasheet_join_factory: Callable[[], Join] = (
    Join(Collection.WEAPON_DATASHEET)
    .on("item_id")
    .to("item_id")
    .inject_at("weapon_datasheet")
    .get_factory()
)
