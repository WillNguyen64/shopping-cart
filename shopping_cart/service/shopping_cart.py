from functools import lru_cache
from sqlalchemy.orm import Session

from .. import schemas
from .. import models


@lru_cache
def get_shopping_cart_service():
    return ShoppingCartService()


class ShoppingCartService:
    def get_items_from_cart(self, db: Session):
        return db.query(models.CartItem).all()

    def add_item_to_cart(self, db: Session, new_item: schemas.CartItemCreate):
        db_item = models.CartItem(**new_item.model_dump())
        db_item.id = None
        db_item.reservation_id = None

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
