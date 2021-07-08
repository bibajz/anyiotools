import anyio
import pytest
from hypothesis import given
from hypothesis import strategies as st

from anyiotools.counters import arange
from anyiotools.mappers import amap
from anyiotools.utils import alist, collect_into_list, ensure_asyncgen, throw_into
from anyiotools.zippers import azip, azip_longest, merge


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_zipping_uneven_length_strict_raises(anyio_backend):
    i = 10
    a1 = arange(i)
    a2 = arange(i + 1)
    with pytest.raises(ValueError):
        await collect_into_list(azip, a1, a2, strict=True)

    assert a1.ag_running is False
    assert a2.ag_running is False


async def test_zipping_being_thrown_into(anyio_backend):
    i = 10
    a1 = arange(i)
    a2 = arange(i + 1)
    with pytest.raises(ValueError):
        await collect_into_list(
            azip,
            throw_into(a1, threshold=0.95, excs=(ValueError,)),
            a2,
        )

    assert a1.ag_running is False
    assert a2.ag_running is False


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_zipping_uneven_length_not_strict_no_warnings(anyio_backend):
    i = 10
    assert len(await collect_into_list(azip, arange(i), arange(i + 5))) == 10


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_zipping_longest_fillvalue_counts(anyio_backend):
    base_len = 10
    collected = await collect_into_list(
        azip_longest,
        arange(base_len),
        arange(base_len + 2),
        arange(base_len + 5),
        fillvalue=None,
    )

    shortest_fillvalue_count = len([i for i in collected if i[0] is None])
    assert shortest_fillvalue_count == 5

    middle_fillvalue_count = len([i for i in collected if i[1] is None])
    assert middle_fillvalue_count == 3

    longest_fillvalue_count = len([i for i in collected if i[2] is None])
    assert longest_fillvalue_count == 0


async def test_merging_lengths(anyio_backend):
    base_len = 10
    collected = await collect_into_list(
        merge,
        arange(base_len),
        arange(base_len + 2),
        arange(base_len + 5),
    )

    assert len(collected) == 2 + 5 + 3 * base_len


async def test_merging_preserves_order_within_asyncgens(anyio_backend, inverse_sleep):
    a1 = ensure_asyncgen([1, 5, 1])
    a2 = ensure_asyncgen([1, 3, 10])
    a3 = ensure_asyncgen([3, 2, 1])

    collected = await collect_into_list(
        merge, amap(inverse_sleep, a1), amap(inverse_sleep, a2), amap(inverse_sleep, a3)
    )

    assert collected == [10, 5, 3, 3, 2, 1, 1, 1, 1]
