from typing import List

import altair
from ps2_census.enums import ItemCategory

from ps2_analysis.weapons.classes.damage_profile import DamageLocation
from ps2_analysis.weapons.classes.infantry_weapon import InfantryWeapon

from .color_selections import FACTION_COLOR, FACTION_SELECTION

X: str = "x"
Y: str = "y"


def generate_infantry_weapons_ttk_to_mhd_plot(
    weapons: List[InfantryWeapon],
    distance: int,
    categories: List[ItemCategory],
    directory: str,
    base_filename: str = "ttk_to_mhd",
):
    def weapon_filter(w: InfantryWeapon):
        return w.category in categories

    # Body shots
    bodyshot_dataset: altair.Data = altair.Data(
        values=[
            {
                "Name": str(w.name),
                X: (
                    w.fire_groups[0].ads_fire_mode.fire_timing.time_to_fire_shots(
                        shots=w.fire_groups[
                            0
                        ].ads_fire_mode.direct_damage_profile.shots_to_kill(
                            distance=distance, location=DamageLocation.TORSO
                        )
                    )
                ),
                Y: w.fire_groups[0].ads_fire_mode.recoil.max_horizontal_deviation,
                "Faction": w.faction.name,
            }
            for w in filter(weapon_filter, weapons)
        ]
    )

    bodyshot_chart: altair.Chart = (
        altair.Chart(bodyshot_dataset)
        .mark_point()
        .encode(
            x=altair.X(f"{X}:Q", axis=altair.Axis(title="time to kill (body shot)")),
            y=altair.Y(f"{Y}:Q", axis=altair.Axis(title="max horizontal deviation")),
            color=FACTION_COLOR,
            tooltip="Name:N",
        )
        .interactive()
    )

    bodyshot_legend: altair.Chart = (
        altair.Chart(bodyshot_dataset)
        .mark_point()
        .encode(
            y=altair.Y("Faction:N", axis=altair.Axis(orient="right")),
            color=FACTION_COLOR,
        )
        .add_selection(FACTION_SELECTION)
    )

    bodyshot_result = altair.hconcat(bodyshot_chart, bodyshot_legend)

    # Head shots
    headshot_dataset: altair.Data = altair.Data(
        values=[
            {
                "Name": str(w.name),
                X: (
                    w.fire_groups[0].ads_fire_mode.fire_timing.time_to_fire_shots(
                        shots=w.fire_groups[
                            0
                        ].ads_fire_mode.direct_damage_profile.shots_to_kill(
                            distance=distance, location=DamageLocation.HEAD
                        )
                    )
                ),
                Y: w.fire_groups[0].ads_fire_mode.recoil.max_horizontal_deviation,
                "Faction": w.faction.name,
            }
            for w in filter(weapon_filter, weapons)
        ]
    )

    headshot_chart: altair.Chart = (
        altair.Chart(headshot_dataset)
        .mark_point()
        .encode(
            x=altair.X(f"{X}:Q", axis=altair.Axis(title="time to kill (head shot)")),
            y=altair.Y(
                f"{Y}:Q", axis=altair.Axis(title="maximum horizontal deviation")
            ),
            color=FACTION_COLOR,
            tooltip="Name:N",
        )
        .interactive()
    )

    headshot_legend: altair.Chart = (
        altair.Chart(headshot_dataset)
        .mark_point()
        .encode(
            y=altair.Y("Faction:N", axis=altair.Axis(orient="right")),
            color=FACTION_COLOR,
        )
        .add_selection(FACTION_SELECTION)
    )

    headshot_result = altair.hconcat(headshot_chart, headshot_legend)

    # Result
    result = altair.vconcat(bodyshot_result, headshot_result)

    result.save(
        f"{directory}/{base_filename}_{'-'.join((c.name for c in categories))}_{distance}m.html"
    )
