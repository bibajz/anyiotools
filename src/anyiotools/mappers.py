from typing import AsyncGenerator, AsyncIterable, Awaitable, Callable, TypeVar

from anyio import create_memory_object_stream, create_task_group
from anyio.abc import TaskGroup
from anyio.streams.memory import MemoryObjectSendStream

A = TypeVar("A")
B = TypeVar("B")


async def amap(
    async_fn: Callable[[A], Awaitable[B]], agen: AsyncGenerator[B, None]
) -> AsyncIterable[B]:
    send_stream, receive_strean = create_memory_object_stream()

    async def apply_and_send(item: A, stream: MemoryObjectSendStream[B]) -> None:
        async with stream:
            await stream.send(await async_fn(item))

    async def consume(task_group: TaskGroup) -> None:
        async with send_stream:
            async for i in agen:
                task_group.start_soon(apply_and_send, i, send_stream.clone())

    async with create_task_group() as tg:
        tg.start_soon(consume, tg)
        async with receive_strean:
            async for i in receive_strean:
                yield i
