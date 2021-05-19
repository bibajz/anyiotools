import pytest

# TODO: Why do I have to set it?
@pytest.fixture(scope="module")
def anyio_backend():
    return "trio"
