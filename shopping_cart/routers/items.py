from fastapi import APIRouter, Depends, BackgroundTasks
from starlette import status
from sqlalchemy.orm import Session

from ..common.logger import get_logger
from ..service.shopping_cart import get_shopping_cart_service
from ..service.reservation import get_reservation_service
from .. import schemas
from .. import models


logger = get_logger(__name__)
shopping_cart_service = get_shopping_cart_service()
reservation_service = get_reservation_service()


def create_items_router():
    router = APIRouter(prefix="")

    @router.get(
        "/items",
        status_code=status.HTTP_200_OK,
        response_model=schemas.CartItemList,
        summary="List items in a cart",
        description="Lists items in a cart",
        response_description="A JSON array of items in the cart",
    )
    async def get_items_from_cart(db: Session = Depends(models.get_db_session)):
        items = shopping_cart_service.get_items_from_cart(db)
        logger.debug(f"Get items: num_items={len(items)}")
        return {"items": items}

    @router.post(
        "/items",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=schemas.CartItemCreate,
        summary="Adds an item to the cart",
        description="Adds a new item to the cart and reserves it",
        response_description="A JSON string of the item added to the cart",
    )
    async def add_item_to_cart(
        order: schemas.CartItemCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(models.get_db_session),
    ):
        item = schemas.CartItemCreate(name=order.name, quantity=order.quantity)
        logger.debug(f"Add item: {item}")
        db_item = shopping_cart_service.add_item_to_cart(db, item)

        # Reserve the item in the background
        item_to_reserve = schemas.CartItem(**db_item.__dict__)
        background_tasks.add_task(reservation_service.reserve_item, item_to_reserve)
        return item

    return router
