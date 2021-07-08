from contextlib import AsyncExitStack
from typing import Any, AsyncGenerator, AsyncIterator, Optional, Tuple

from anyio import create_memory_object_stream, create_task_group
from anyio.streams.memory import MemoryObjectSendStream

from ._compat import aclosing


async def azip(
    *agens: AsyncGenerator,
    strict: bool = False,
) -> AsyncGenerator[Tuple, None]:
    """
    Zip async generators to produce an async generator of tuples.

    Each step runs concurrently in `anyio.TaskGroup`.

    If the aiters are of uneven length and `strict` is set to True, `ValueError`
    is raised. Otherwise, (potential) inconsistency is ignored, but closing of all
    the async generators is **always** done.
    """
    n = len(agens)

    consumed = 0
    # TODO: Will be filled by yielded values from iterators - not ideal,
    #   probably rework later.
    items = [None for _ in range(n)]

    async def advance(ag: AsyncGenerator, idx: int) -> None:
        nonlocal consumed
        try:
            item = await ag.__anext__()
        except StopAsyncIteration:
            consumed += 1
        else:
            items[idx] = item

    async with AsyncExitStack() as astack:
        aclosing_agens = [
            await astack.enter_async_context(aclosing(ag)) for ag in agens
        ]
        while True:
            async with create_task_group() as tg:
                for i, ag in enumerate(aclosing_agens):
                    tg.start_soon(advance, ag, i)

            if consumed == 0:
                yield tuple(items)
            else:
                if strict and consumed != n:
                    raise ValueError("Async iterators of unever length provided!")
                else:
                    break


async def azip_longest(
    *agens: AsyncGenerator,
    fillvalue: Optional[Any] = None,
) -> AsyncIterator[Tuple]:
    """
    Zip async generators to produce an async generator of tuples.

    Each step runs concurrently in `anyio.TaskGroup`.

    If the aiters are of uneven length, the consumed ones are filled with
    `fillvalue`.
    """
    n = len(agens)

    consumed = [False for _ in range(n)]
    items = [fillvalue for _ in range(n)]

    async def consume(ag: AsyncGenerator, i: int) -> None:
        try:
            item = await ag.__anext__()
        except StopAsyncIteration:
            consumed[i] = True
            items[i] = fillvalue
        else:
            items[i] = item

    while True:
        async with create_task_group() as tg:
            for i, ag in enumerate(agens):
                if not consumed[i]:
                    tg.start_soon(consume, ag, i)

        if all(consumed):
            break
        else:
            yield tuple(items)


async def merge(*agens: AsyncGenerator) -> AsyncGenerator:
    """
    Multiple producers single consumer pattern
    """
    send_stream, receive_strean = create_memory_object_stream()

    async def consume(ag: AsyncGenerator, stream: MemoryObjectSendStream) -> None:
        async with stream:
            async for i in ag:
                await stream.send(i)

    async with create_task_group() as tg:
        with send_stream:
            for ag in agens:
                tg.start_soon(consume, ag, send_stream.clone())

        async with receive_strean:
            async for i in receive_strean:
                yield i
