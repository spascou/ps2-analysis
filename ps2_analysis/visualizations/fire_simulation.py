from typing import List, Tuple

import altair

from ps2_analysis.weapons.classes.infantry_weapon import InfantryWeapon

from .color_selections import (
    SIMULATION_POINT_TYPE_COLOR,
    SIMULATION_POINT_TYPE_SELECTION,
)

X: str = "x"
Y: str = "y"


def generate_infantry_weapon_fire_simulation_plot(
    weapon: InfantryWeapon,
    shots: int,
    runs: int,
    directory: str,
    base_filename: str = "infantry_weapon_fire_simulation",
):

    datapoints: List[dict] = []

    for simulation in [
        weapon.fire_groups[0].ads_fire_mode.simulate_shots(shots=shots)
        for _ in range(runs)
    ]:
        t: int
        cursor_coor: Tuple[float, float]
        pellets_coors: List[Tuple[float, float]]
        for t, cursor_coor, pellets_coors in simulation:
            cursor_x, cursor_y = cursor_coor

            datapoints.append({"Time": t, X: cursor_x, Y: cursor_y, "Type": "cursor"})
            for pellet_x, pellet_y in pellets_coors:
                datapoints.append(
                    {"Time": t, X: pellet_x, Y: pellet_y, "Type": "pellet"}
                )

    dataset: altair.Data = altair.Data(values=datapoints)

    chart: altair.Chart = (
        altair.Chart(dataset)
        .mark_point()
        .encode(
            x=altair.X(f"{X}:Q", axis=altair.Axis(title="horizontal angle")),
            y=altair.Y(f"{Y}:Q", axis=altair.Axis(title="vertical angle")),
            color=SIMULATION_POINT_TYPE_COLOR,
            tooltip="Time:Q",
        )
        .interactive()
    )

    legend: altair.Chart = (
        altair.Chart(dataset)
        .mark_point()
        .encode(
            y=altair.Y("Type:N", axis=altair.Axis(orient="right")),
            color=SIMULATION_POINT_TYPE_COLOR,
        )
        .add_selection(SIMULATION_POINT_TYPE_SELECTION)
    )

    result = altair.hconcat(chart, legend)

    result.save(f"{directory}/{base_filename}_{weapon.slug}_{runs}x{shots}.html")
