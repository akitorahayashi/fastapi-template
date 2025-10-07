import pytest


@pytest.fixture(autouse=True)
def setup_unit_test(setup_unit_test_env):
    """Set environment variables for unit tests."""
    pass
