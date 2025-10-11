import httpx


class TestIntgAPI:
    """
    Class-based integration tests for API endpoints.
    Tests run against the local server started by conftest.py.
    """

    def test_intg_hello_world(self, api_base_url: str):
        """Integration smoke test for hello world endpoint."""
        with httpx.Client(base_url=api_base_url) as client:
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "Hello World"}

    def test_intg_health_check(self, api_base_url: str):
        """Integration smoke test for health check endpoint."""
        with httpx.Client(base_url=api_base_url) as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
