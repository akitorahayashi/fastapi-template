import time
import httpx
from testcontainers.compose import DockerCompose


def test_e2e_hello_world():
    """End-to-end smoke test for hello world endpoint using docker compose."""
    with DockerCompose(".", compose_file_name="docker-compose.yml") as compose:
        # Wait for services to be ready
        time.sleep(10)
        
        # Get the exposed port for the API service
        api_port = compose.get_service_port("api", 8000)
        base_url = f"http://localhost:{api_port}"
        
        with httpx.Client(base_url=base_url) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}


def test_e2e_health_check():
    """End-to-end smoke test for health check endpoint using docker compose."""
    with DockerCompose(".", compose_file_name="docker-compose.yml") as compose:
        # Wait for services to be ready
        time.sleep(10)
        
        # Get the exposed port for the API service
        api_port = compose.get_service_port("api", 8000)
        base_url = f"http://localhost:{api_port}"
        
        with httpx.Client(base_url=base_url) as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}