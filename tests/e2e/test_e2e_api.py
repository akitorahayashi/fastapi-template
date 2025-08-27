import os

import httpx
import pytest

# Mark all tests in this file as asyncio
pytestmark = pytest.mark.asyncio

BASE_URL = f"http://localhost:{os.getenv('HOST_PORT', '8000')}"


async def test_health_check_e2e():
    """
    Tests the /health endpoint to ensure the service is running.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_items_crud_e2e():
    """
    Performs an end-to-end CRUD test on the /api/v1/items/ endpoint.
    """
    item_payload = {"name": "E2E Test Item", "description": "A test item from E2E."}
    item_id = None

    async with httpx.AsyncClient(timeout=20) as client:
        # 1. Create Item
        response = await client.post(f"{BASE_URL}/api/v1/items/", json=item_payload)
        assert response.status_code == 201
        created_item = response.json()
        item_id = created_item["id"]
        assert created_item["name"] == item_payload["name"]

        # 2. Read Item
        response = await client.get(f"{BASE_URL}/api/v1/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == item_payload["name"]

        # 3. Read Items
        response = await client.get(f"{BASE_URL}/api/v1/items/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0

        # 4. Update Item
        update_payload = {"name": "Updated E2E Item", "description": "Updated desc."}
        response = await client.put(
            f"{BASE_URL}/api/v1/items/{item_id}", json=update_payload
        )
        assert response.status_code == 200
        assert response.json()["name"] == update_payload["name"]

        # 5. Delete Item
        response = await client.delete(f"{BASE_URL}/api/v1/items/{item_id}")
        assert response.status_code == 200

        # 6. Verify Deletion
        response = await client.get(f"{BASE_URL}/api/v1/items/{item_id}")
        assert response.status_code == 404
