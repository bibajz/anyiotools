import pytest
from hypothesis import given
from hypothesis import strategies as st

from anyiotools.counters import arange
from anyiotools.utils import collect_into_list
from anyiotools.zippers import azip, azip_longest


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_zipping_uneven_length_strict_raises(anyio_backend):
    i = 10
    with pytest.raises(ValueError):
        await collect_into_list(azip, arange(i), arange(i + 1), strict=True)


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_zipping_uneven_length_not_strict_no_warnings(anyio_backend):
    i = 10
    assert len(await collect_into_list(azip, arange(i), arange(i + 5))) == 10


# TODO: How to use `hypothesis` with `pytest-asyncio`?
# @given(st.integers(min_value=0))
async def test_def_zipping_longest_fillvalue_counts(anyio_backend):
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
