import pytest

from tests.envs import setup_unit_test_env


@pytest.fixture(autouse=True)
def setup_unit_test(monkeypatch):
    """Setup environment variables for unit tests."""
    setup_unit_test_env(monkeypatch)
