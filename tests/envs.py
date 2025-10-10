"""Environment variable configuration for different test categories."""


def setup_unit_test_env(monkeypatch):
    """Setup environment variables for unit tests."""
    monkeypatch.setenv("USE_SQLITE", "true")
    # Add mock settings here if external services are added in the future
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "true")


def setup_db_test_env(monkeypatch):
    """Setup environment variables for database tests."""
    # USE_SQLITE is passed from justfile, so not set here
    pass
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "true")


def setup_e2e_test_env(monkeypatch):
    """Setup environment variables for E2E tests - use real services."""
    monkeypatch.setenv("USE_SQLITE", "false")
    # E2E tests are expected to use real services
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "false")