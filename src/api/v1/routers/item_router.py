from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.api.v1.schemas.item_schema import ItemCreate, ItemRead, ItemUpdate
from src.api.v1.services import item_service
from src.db.database import get_db

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db)):
    return item_service.create_item(db=db, item=item)


@router.get("/", response_model=list[ItemRead])
def read_items_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = item_service.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=ItemRead)
def read_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = item_service.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/{item_id}", response_model=ItemRead)
def update_item_endpoint(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = item_service.update_item(db, item_id=item_id, item_data=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}", response_model=ItemRead)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = item_service.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
