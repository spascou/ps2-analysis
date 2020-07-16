import decimal
import functools
import math
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Union,
)

from ps2_census.enums import ResistType

from .data import DAMAGE_TARGET_TYPE_DATA
from .enums import DamageLocation, DamageTargetType


def discover(data: Iterable[dict], path: str = "") -> Dict[str, Set[str]]:

    res: Dict[str, Set[str]] = {}

    for d in data:

        for key, value in d.items():

            new_path = ".".join((path, key))

            if isinstance(value, dict):
                d_res: Dict[str, Set[str]] = discover(data=(value,), path=new_path)

                for k, v in d_res.items():

                    if k in res:

                        res[k] = res[k].union(v)

                    else:

                        res[k] = v

            elif isinstance(value, list):
                l_res: Dict[str, Set[str]] = discover(data=value, path=new_path)

                for k, v in l_res.items():

                    if k in res:

                        res[k] = res[k].union(v)

                    else:

                        res[k] = v

            else:

                if new_path in res:

                    res[new_path].add(value)

                else:

                    res[".".join((path, key))] = {value}

    return res


def get(mapping: Mapping, key: str, typer: Callable[[str], Any]) -> Any:

    return typer(mapping[key])


def optget(
    mapping: Mapping,
    key: str,
    typer: Callable[[str], Any],
    default: Optional[Any] = None,
) -> Any:

    if key in mapping:

        return get(mapping=mapping, key=key, typer=typer)

    else:

        return default


@functools.lru_cache
def float_range_list(
    start: Union[int, float],
    stop: Union[int, float],
    step: Union[int, float],
    precision_decimals: int = 2,
) -> List[float]:

    result: List[float] = []

    start_d = decimal.Decimal(start)
    stop_d = decimal.Decimal(stop)

    while start_d < stop_d:

        result.append(round(float(start_d), precision_decimals))

        start_d += decimal.Decimal(step)

    return result


def float_range(
    start: Union[int, float],
    stop: Union[int, float],
    step: Union[int, float],
    precision_decimals: int = 2,
) -> Iterator[float]:

    yield from float_range_list(
        start=start, stop=stop, step=step, precision_decimals=precision_decimals
    )


@functools.lru_cache
def apply_damage_resistance(damage: int, resistance: float = 0.0) -> int:

    if resistance < 1.0:

        # Damage reduced by resistances is rounded up
        return int(math.ceil(damage * (1 - resistance)))

    else:

        return 0


@functools.lru_cache
def locational_linear_falloff(
    x: float, x_0: float, y_0: float, x_1: float, y_1: float
) -> float:

    if y_0 == y_1 or x <= x_0:

        return y_0

    elif x >= x_1:

        return y_1

    else:

        return y_1 * (1 - (x - x_1) / (x_0 - x_1)) + y_0 * ((x - x_1) / (x_0 - x_1))


@functools.lru_cache
def resolve_damage_resistance(
    damage_target_type: DamageTargetType,
    damage_location: DamageLocation,
    resist_type: ResistType,
    damage_target_type_data: Dict[
        DamageTargetType, Dict[str, Any]
    ] = DAMAGE_TARGET_TYPE_DATA,
) -> float:

    if damage_target_type in damage_target_type_data:

        data: dict = damage_target_type_data[damage_target_type]

        if "damage_resistance" in data:

            resistance_data: dict = data["damage_resistance"]

            location_info: Union[str, DamageLocation, set]
            location_resistance_data: dict
            for location_info, location_resistance_data in resistance_data.items():

                if (
                    "any" == location_info
                    or damage_location == location_info
                    or damage_location in location_info
                ):

                    resist_type_info: Union[str, ResistType, set]
                    resistance: float
                    for (
                        resist_type_info,
                        resistance,
                    ) in location_resistance_data.items():

                        if (
                            "any" == resist_type_info
                            or resist_type == resist_type_info
                            or resist_type in resist_type_info
                        ):

                            return resistance

            return 0.0

        else:

            return 0.0

    else:

        raise ValueError(f"{damage_target_type} has no data")


@functools.lru_cache
def resolve_health_pool(
    damage_target_type: DamageTargetType,
    damage_target_type_data: Dict[
        DamageTargetType, Dict[str, Any]
    ] = DAMAGE_TARGET_TYPE_DATA,
) -> int:

    if damage_target_type in damage_target_type_data:

        data: dict = damage_target_type_data[damage_target_type]

        return data.get("health", 0) + data.get("shields", 0)

    else:

        raise ValueError(f"{damage_target_type} has no data")


def all_equal(elements: Iterable[Any]) -> bool:

    elements_it = iter(elements)

    try:

        first = next(elements_it)

    except StopIteration:

        return True

    return all(first == rest for rest in elements_it)
