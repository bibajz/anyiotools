import anyio
import pytest


# TODO: Why do I have to set it?
@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def inverse_sleep():
    async def wrapped(n: int) -> int:
        await anyio.sleep(1/n)
        return n

    return wrapped
