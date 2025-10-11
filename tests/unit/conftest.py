import pytest


@pytest.fixture(autouse=True)
def setup_unit_test(monkeypatch):
    """Setup environment variables for unit tests.

    Note: Monkeypatch only works for in-process execution.
    For subprocess-based tests, use subprocess env parameter.
    """
    monkeypatch.setenv("USE_SQLITE", "true")
    # Add mock settings here if external services are added in the future
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "true")
