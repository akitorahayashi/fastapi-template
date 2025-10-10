"""Environment variable configuration for different test categories."""

import pytest


@pytest.fixture
def setup_unit_test_env(monkeypatch):
    """Setup environment variables for unit tests."""
    monkeypatch.setenv("USE_SQLITE", "true")
    # Add mock settings here if external services are added in the future
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "true")


@pytest.fixture
def setup_db_test_env(monkeypatch):
    """Setup environment variables for database tests."""
    # USE_SQLITE is passed from justfile, so not set here
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "true")


@pytest.fixture
def setup_intg_test_env(monkeypatch):
    """Setup environment variables for integration tests."""
    monkeypatch.setenv("USE_SQLITE", "true")


@pytest.fixture
def setup_e2e_test_env(monkeypatch):
    """Setup environment variables for E2E tests - use real services."""
    monkeypatch.setenv("USE_SQLITE", "false")
    # E2E tests are expected to use real services
    # monkeypatch.setenv("USE_MOCK_SERVICE_A", "false")
