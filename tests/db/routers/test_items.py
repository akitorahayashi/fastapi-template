from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.api.v1.schemas.item_schema import ItemCreate
from src.api.v1.services import item_service


def test_create_item(db: Session):
    item_in = ItemCreate(name="Test Item", description="Test Description")
    item = item_service.create_item(db, item=item_in)
    assert item.name == item_in.name
    assert item.description == item_in.description
    assert item.id is not None


def test_get_item(db: Session):
    item_in = ItemCreate(name="Test Get Item", description="Test Get Description")
    item = item_service.create_item(db, item=item_in)
    retrieved_item = item_service.get_item(db, item_id=item.id)
    assert retrieved_item
    assert retrieved_item.id == item.id
    assert retrieved_item.name == item.name


def test_get_items(db: Session):
    item_service.create_item(db, item=ItemCreate(name="Item 1"))
    item_service.create_item(db, item=ItemCreate(name="Item 2"))
    items = item_service.get_items(db, skip=0, limit=10)
    assert len(items) >= 2


def test_item_api_endpoints(client: TestClient):
    # Create an item
    response = client.post(
        "/api/v1/items/", json={"name": "API Item", "description": "API Description"}
    )
    assert response.status_code == 201
    data = response.json()
    item_id = data["id"]
    assert data["name"] == "API Item"

    # Get the item
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "API Item"

    # Get all items
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert len(response.json()) > 0

    # Update the item
    response = client.put(
        f"/api/v1/items/{item_id}",
        json={"name": "Updated API Item", "description": "Updated Description"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated API Item"

    # Delete the item
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated API Item"

    # Verify deletion
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404
