import pytest

@pytest.fixture(autouse=True)
def setup_unit_test(monkeypatch):
    """Set environment variables for unit tests."""
    from tests.envs import setup_unit_test_env
    setup_unit_test_env(monkeypatch)