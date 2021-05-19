import itertools
from typing import AsyncIterator, TypeVar, Union

T = TypeVar("T")

# TODO: put it to separate module later. Also, `itertools.count` supports
#   `decimal.Decimal` (as an example), so maybe expand later
Number = Union[int, float]


async def acount(start: Number = 0, step: Number = 1) -> AsyncIterator[Number]:
    for i in itertools.count(start, step):
        yield i


async def arange(*args: int) -> AsyncIterator[int]:
    for i in range(*args):
        yield i
