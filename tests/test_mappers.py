import pytest

from anyiotools.counters import arange
from anyiotools.mappers import amap


@pytest.mark.anyio
async def test_amap_does_not_preserve_order(inverse_sleep):

    res = [i async for i in amap(inverse_sleep, arange(1, 6))]
    assert res == [5, 4, 3, 2, 1]
