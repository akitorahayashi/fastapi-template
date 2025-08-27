import time
import httpx
import pytest
from testcontainers.compose import DockerCompose

COMPOSE_FILE = "docker-compose.yml"
API_SERVICE = "api"
API_PORT = 8000
HEALTHCHECK_TIMEOUT = 120  # 120 seconds
HEALTHCHECK_INTERVAL = 1  # 1 second


def _wait_for_health_check(compose: DockerCompose):
    """
    Waits for the API service to become healthy by polling its /health endpoint.
    """
    api_port = compose.get_service_port(API_SERVICE, API_PORT)
    base_url = f"http://localhost:{api_port}"
    start_time = time.time()

    while time.time() - start_time < HEALTHCHECK_TIMEOUT:
        try:
            with httpx.Client(base_url=base_url) as client:
                response = client.get("/health")
                if response.status_code == 200 and response.json() == {"status": "ok"}:
                    print(f"API service is healthy after {time.time() - start_time:.2f}s.")
                    return
        except httpx.ConnectError:
            # Service is not yet ready, wait and retry
            pass
        time.sleep(HEALTHCHECK_INTERVAL)

    # If the loop completes, the health check has timed out
    logs = compose.get_logs()
    print("API service health check timed out.")
    print("="*80)
    for service, log in logs.items():
        print(f"Logs for {service}:")
        print(log.decode('utf-8'))
        print("-" * 80)
    pytest.fail(f"API service did not become healthy within {HEALTHCHECK_TIMEOUT} seconds.")


@pytest.fixture(scope="module")
def api_base_url():
    """
    Starts the Docker Compose stack, waits for it to be healthy,
    and provides the base URL for the API service.
    """
    with DockerCompose(".", compose_file_name=COMPOSE_FILE) as compose:
        _wait_for_health_check(compose)
        api_port = compose.get_service_port(API_SERVICE, API_PORT)
        yield f"http://localhost:{api_port}"


def test_e2e_hello_world(api_base_url: str):
    """End-to-end smoke test for hello world endpoint."""
    with httpx.Client(base_url=api_base_url) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}


def test_e2e_health_check(api_base_url: str):
    """End-to-end smoke test for health check endpoint."""
    with httpx.Client(base_url=api_base_url) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
