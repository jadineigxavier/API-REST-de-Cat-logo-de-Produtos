from typing import List, Optional

from sqlmodel import Session, select

from . import models, schemas
from .utils import placeholder_image


def list_items(
    session: Session,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[models.Item]:
    query = select(models.Item)
    if category:
        query = query.where(models.Item.category == category)
    return session.exec(query.offset(skip).limit(limit)).all()


def get_item(session: Session, item_id: int) -> Optional[models.Item]:
    return session.get(models.Item, item_id)


def create_item(session: Session, item_in: schemas.ItemCreate) -> models.Item:
    data = item_in.model_dump()
    if not data.get("image_url"):
        data["image_url"] = placeholder_image(data["name"])
    item = models.Item(**data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_item(
    session: Session, item: models.Item, item_in: schemas.ItemUpdate
) -> models.Item:
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def delete_item(session: Session, item: models.Item) -> None:
    session.delete(item)
    session.commit()
