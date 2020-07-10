import decimal
import math
from typing import Any, Callable, Dict, Iterable, Mapping, Optional, Set, Union


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


def get(mapping: Mapping, key: str, typer: Callable[[str], Any]):
    return typer(mapping[key])


def optget(
    mapping: Mapping,
    key: str,
    typer: Callable[[str], Any],
    default: Optional[Any] = None,
):
    if key in mapping:

        return get(mapping=mapping, key=key, typer=typer)

    else:

        return default


def float_range(
    start: Union[int, float],
    stop: Union[int, float],
    step: Union[int, float],
    precision_decimals: int = 2,
):
    start_d = decimal.Decimal(start)
    stop_d = decimal.Decimal(stop)

    while start_d < stop_d:

        yield round(float(start_d), precision_decimals)

        start_d += decimal.Decimal(step)


def damage_to_kill(
    health: int = 500, shields: int = 500, damage_resistance: float = 0.0
) -> int:

    if damage_resistance < 1.0:

        return math.ceil((health + shields) / (math.ceil(1 - damage_resistance)))

    else:

        return -1
