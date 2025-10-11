import os
import subprocess
import sys
import time

import httpx
import pytest
from dotenv import load_dotenv

from tests.envs import setup_intg_test_env

# Load .env file to get port configuration
load_dotenv()

TEST_HOST = os.getenv("FAPI_SANDBOX_HOST_IP", "127.0.0.1")
TEST_PORT = int(os.getenv("FAPI_SANDBOX_HOST_PORT", "8080"))


@pytest.fixture(autouse=True)
def set_intg_test_env(monkeypatch):
    """Setup environment variables for integration tests."""
    setup_intg_test_env(monkeypatch)


@pytest.fixture(scope="session")
def api_base_url():
    """
    Provides the base URL for the API service.
    """
    return f"http://{TEST_HOST}:{TEST_PORT}"


@pytest.fixture(scope="session", autouse=True)
def start_server():
    process = None
    try:
        # Start server in subprocess instead of thread for proper cleanup

        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "src.main:app",
                "--host",
                TEST_HOST,
                "--port",
                str(TEST_PORT),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for server to be ready by polling health endpoint
        max_attempts = 10
        attempt = 0
        health_url = f"http://{TEST_HOST}:{TEST_PORT}/health"
        while attempt < max_attempts:
            try:
                response = httpx.get(health_url, timeout=1.0)
                if response.status_code == 200:
                    break
            except httpx.RequestError:
                pass
            time.sleep(0.5)
            attempt += 1
        else:
            if process:
                process.terminate()
            raise RuntimeError("Server did not start within expected time")

        yield

    finally:
        # Cleanup: terminate the server process
        if process:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
