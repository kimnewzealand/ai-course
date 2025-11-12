from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app import models, schemas
from datetime import datetime

def get_items(db: Session, limit: int = 10, offset: int = 0):
    result = db.execute(select(models.Item).offset(offset).limit(limit))
    db_items = result.scalars().all()
    return [schemas.Item(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        created_at=item.created_at,
        updated_at=item.updated_at
    ) for item in db_items]

def get_item(db: Session, item_id: int):
    result = db.execute(select(models.Item).where(models.Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item:
        return schemas.Item(
            id=db_item.id,
            name=db_item.name,
            description=db_item.description,
            price=db_item.price,
            created_at=db_item.created_at,
            updated_at=db_item.updated_at
        )
    return None

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump(), created_at=datetime.utcnow().isoformat(), updated_at=None)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return schemas.Item(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        price=db_item.price,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at
    )

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    stmt = (
        update(models.Item)
        .where(models.Item.id == item_id)
        .values(**item.model_dump(), updated_at=datetime.utcnow().isoformat())
    )
    db.execute(stmt)
    db.commit()
    
    result = db.execute(select(models.Item).where(models.Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item:
        return schemas.Item(
            id=db_item.id,
            name=db_item.name,
            description=db_item.description,
            price=db_item.price,
            created_at=db_item.created_at,
            updated_at=db_item.updated_at
        )
    return None

def delete_item(db: Session, item_id: int):
    result = db.execute(
        delete(models.Item).where(models.Item.id == item_id)
    )
    db.commit()
    return result.rowcount > 0
