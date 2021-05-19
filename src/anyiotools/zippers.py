from typing import Any, AsyncIterator, Optional, Tuple

from anyio import create_task_group


async def azip(*aits: AsyncIterator, strict: bool = False) -> AsyncIterator[Tuple]:
    """
    Zip async iterators to produce an async iterator of tuples.

    Each step runs concurrently in `anyio.TaskGroup`.

    If the aiters are of uneven length and `strict` is set to True, `ValueError`
    is raised. Otherwise, (potential) inconsistency is silently ignored.
    """
    n = len(aits)

    consumed = 0
    # TODO: Will be filled by yielded values from iterators - not ideal,
    #   probably rework later.
    items = [None for _ in range(n)]

    async def consume(ait: AsyncIterator, i: int) -> None:
        nonlocal consumed
        try:
            item = await ait.__anext__()
        except StopAsyncIteration:
            consumed += 1
        else:
            items[i] = item

    while True:
        async with create_task_group() as tg:
            for i, ait in enumerate(aits):
                tg.start_soon(consume, ait, i)

        if consumed > 0:
            if strict and consumed != n:
                raise ValueError("Async iterators of unever length provided!")
            else:
                break
        else:
            yield tuple(items)


async def azip_longest(
    *aits: AsyncIterator, fillvalue: Optional[Any] = None
) -> AsyncIterator[Tuple]:
    """
    Zip async iterators to produce an async iterator of tuples.

    Each step runs concurrently in `anyio.TaskGroup`.

    If the aiters are of uneven length, the consumed ones are padded with
    `fillvalue`.
    """
    n = len(aits)

    consumed = [False for _ in range(n)]
    items = [fillvalue for _ in range(n)]

    async def consume(ait: AsyncIterator, i: int) -> None:
        try:
            item = await ait.__anext__()
        except StopAsyncIteration:
            consumed[i] = True
            items[i] = fillvalue
        else:
            items[i] = item

    while True:
        async with create_task_group() as tg:
            for i, ait in enumerate(aits):
                if not consumed[i]:
                    tg.start_soon(consume, ait, i)

        if all(consumed):
            break
        else:
            yield tuple(items)
