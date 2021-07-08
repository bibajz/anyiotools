import inspect
from typing import AsyncGenerator, AsyncIterable, AsyncIterator

import pytest

from anyiotools.counters import arange
from anyiotools.utils import ensure_asyncgen


@pytest.mark.anyio
async def test_aiter_():
    l = [i async for i in ensure_asyncgen(range(10))]
    assert sum(l) == 45


@pytest.mark.anyio
async def test_aiter_on_aiter():
    l = [i async for i in ensure_asyncgen(arange(10))]
    assert sum(l) == 45

    assert inspect.isasyncgenfunction(arange)
    assert inspect.isasyncgen(ensure_asyncgen(range(10)))

    assert inspect.isasyncgen(ensure_asyncgen(arange(10)))

    assert inspect.isasyncgen(arange(10))


@pytest.mark.anyio
async def test_aiter_idempotence():
    agen = ensure_asyncgen(range(10))
    assert agen == ensure_asyncgen(agen)

    assert hasattr(agen, "__aiter__")
    assert hasattr(agen, "__anext__")

    assert isinstance(agen, AsyncIterable)
    assert isinstance(agen, AsyncIterator)
    assert isinstance(agen, AsyncGenerator)
