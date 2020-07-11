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
def damage_to_kill(
    health: int = 500, shields: int = 500, damage_resistance: float = 0.0
) -> int:

    if damage_resistance < 1.0:

        return math.ceil((health + shields) / (math.ceil(1 - damage_resistance)))

    else:

        return -1


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
