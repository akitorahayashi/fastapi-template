import pytest

@pytest.fixture(autouse=True)
def setup_intg_test(monkeypatch):
    """Set environment variables for integration tests."""
    from tests.envs import setup_intg_test_env
    setup_intg_test_env(monkeypatch)