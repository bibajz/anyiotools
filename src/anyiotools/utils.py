import random
from typing import AsyncIterator, Callable, List, TypeVar

import anyio

T = TypeVar("T")


async def collect_into_list(async_fn, *args, **kwargs) -> List:
    """
    Helper coroutine for consuming an async iterator-producing coroutine into
    a list.
    """
    return [i async for i in async_fn(*args, **kwargs)]


async def sleep_walk(
    ait: AsyncIterator[T], delay_fn: Callable[[], float] = random.random
) -> AsyncIterator[T]:
    """
    Helper async generator for iteration with a small time delay introduced.

    TODO: May be promoted to some `delay`/`spaceout` later.
    """
    async for i in ait:
        yield i
        await anyio.sleep(delay_fn())
