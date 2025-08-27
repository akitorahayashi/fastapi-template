from sqlalchemy.orm import Session

from src.api.v1.schemas.item_schema import ItemCreate, ItemUpdate
from src.db.models.item import Item


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return db.query(Item).offset(skip).limit(limit).all()


def update_item(db: Session, item_id: int, item_data: ItemUpdate) -> Item | None:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = item_data.name
        db_item.description = item_data.description
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> Item | None:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
