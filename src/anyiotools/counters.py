import itertools
from typing import AsyncGenerator, Callable, Tuple, TypeVar, Union

from anyiotools.utils import aiter_

__all__ = (
    "acount",
    "aenumerate",
    "arange",
)


T = TypeVar("T")

# TODO: put it to separate module later. Also, `itertools.count` supports
#   `decimal.Decimal` (as an example), so maybe expand later
Number = Union[int, float]

acount: Callable[[Number, Number], AsyncGenerator[Number, None]] = aiter_(
    itertools.count
)
aenumerate: Callable[[T, int], AsyncGenerator[Tuple[int, T], None]] = aiter_(enumerate)
arange: Callable[..., AsyncGenerator[int, None]] = aiter_(range)
