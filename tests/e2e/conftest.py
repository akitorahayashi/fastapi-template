import os
import subprocess
import time
from typing import Generator

import httpx
import pytest
from dotenv import load_dotenv

from tests.envs import setup_e2e_test_env

# Load .env file to get Docker Compose port configuration
load_dotenv()

TEST_HOST = os.getenv("FAPI_TEMPL_HOST_BIND_IP", "127.0.0.1")
TEST_PORT = int(os.getenv("FAPI_TEMPL_TEST_PORT", "8002"))


@pytest.fixture(autouse=True)
def setup_e2e_test(monkeypatch):
    """Setup environment variables for E2E tests."""
    setup_e2e_test_env(monkeypatch)


@pytest.fixture(scope="session")
def api_base_url():
    """
    Provides the base URL for the API service.
    Uses the e2e_setup fixture for container management.
    """
    return f"http://{TEST_HOST}:{TEST_PORT}"


def _is_service_ready(url: str, expected_status: int = 200) -> bool:
    """Check if HTTP service is ready by making a request."""
    try:
        response = httpx.get(url, timeout=5)
        if response.status_code == expected_status:
            return True
    except httpx.RequestError:
        return False
    return False


def _wait_for_service(url: str, timeout: int = 120, interval: int = 5) -> None:
    """Wait for HTTP service to be ready with timeout."""
    print(f"Waiting for service to be ready at {url}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        if _is_service_ready(url):
            print(f"✅ Service at {url} is ready!")
            return
        print(f"⏳ Service not yet ready, retrying in {interval}s...")
        time.sleep(interval)
    raise TimeoutError(
        f"Service at {url} did not become ready within {timeout} seconds"
    )


@pytest.fixture(scope="session", autouse=True)
def e2e_setup(monkeypatch) -> Generator[None, None, None]:
    """
    Manages the lifecycle of the application for end-to-end testing.
    This fixture assumes 'make e2e-test' will manage the containers,
    but it performs the health check wait just in case.
    """
    monkeypatch.setenv("USE_SQLITE", "false")

    health_url = f"http://{TEST_HOST}:{TEST_PORT}/health"

    project_name = os.getenv("FAPI_TEMPL_PROJECT_NAME", "fapi-tmpl")
    test_project_name = f"{project_name}-test"

    # Define base compose command
    base_compose_command = [
        "docker",
        "compose",
        "-f",
        "docker-compose.yml",
        "-f",
        "docker-compose.test.override.yml",
        "--project-name",
        test_project_name,
    ]

    # Define compose commands
    compose_up_command = base_compose_command + ["up", "-d", "--build"]
    compose_down_command = base_compose_command + ["down", "--remove-orphans"]

    try:
        print("\n🚀 Starting E2E test services with docker-compose...")
        subprocess.run(compose_up_command, check=True, timeout=300)

        _wait_for_service(health_url, timeout=30, interval=5)

        yield

    except (subprocess.CalledProcessError, TimeoutError) as e:
        print(f"\n🛑 E2E setup failed: {e}")
        subprocess.run(compose_down_command, check=False)  # Attempt cleanup
        pytest.fail(f"E2E setup failed: {e}")

    finally:
        # Stop services
        print("\n🛑 Stopping E2E services...")
        subprocess.run(compose_down_command, check=False)
