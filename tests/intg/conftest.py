import pytest


@pytest.fixture(autouse=True)
def setup_intg_test(setup_intg_test_env):
    """Set environment variables for integration tests."""
    pass
