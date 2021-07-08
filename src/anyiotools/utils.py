import inspect
import random
from functools import wraps
from typing import (
    AsyncGenerator,
    Callable,
    Iterator,
    List,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

import anyio

T = TypeVar("T")
AsyncGenT = AsyncGenerator[T, None]


async def collect_into_list(async_fn, *args, **kwargs) -> List:
    """
    Helper coroutine for collecting an async iterator-producing coroutine into
    a list.
    """
    return [i async for i in async_fn(*args, **kwargs)]


async def sleep_walk(
    agen: AsyncGenT, delay_fn: Callable[[], float] = random.random
) -> AsyncGenT:
    """
    Helper async generator for iteration with a small time delay introduced.

    TODO: May be promoted to some `delay`/`spaceout` later.
    """
    async for i in agen:
        yield i
        await anyio.sleep(delay_fn())


def aiter_(
    gen_or_agen_fn: Union[Callable[..., Iterator[T]], Type]
) -> Union[Callable[..., AsyncGenT], AsyncGenT]:
    if inspect.isasyncgenfunction(gen_or_agen_fn):
        return cast(AsyncGenT, gen_or_agen_fn)
    else:

        @wraps(gen_or_agen_fn)
        async def wrapper(*args, **kwargs) -> AsyncGenT:
            for i in gen_or_agen_fn(*args, **kwargs):
                yield i

        return wrapper


def ensure_asyncgen(gen_or_agen: Union[Iterator[T], AsyncGenT]):
    if inspect.isasyncgen(gen_or_agen):
        return cast(AsyncGenT, gen_or_agen)
    else:

        async def wrapper() -> AsyncGenT:
            for i in gen_or_agen:
                yield i

        return wrapper()


async def throw_into(
    it_or_ait: Union[Iterator, AsyncGenerator],
    threshold: float = 0.1,
    excs: Sequence[Type[BaseException]] = (Exception,),
):
    agen = ensure_asyncgen(it_or_ait)
    async for i in agen:
        yield i
        if random.random() < threshold:
            await agen.athrow(random.choice(excs))


async def alist(gen_or_agen: Union[Iterator, AsyncGenerator]) -> List:
    return [i async for i in ensure_asyncgen(gen_or_agen)]
