from functools import lru_cache

import httpx
import asyncio
from sqlalchemy.orm import Session
from fastapi import status

from ..common.logger import get_logger
from ..common.settings import get_settings
from .. import schemas
from .. import models


logger = get_logger(__name__)
settings = get_settings()


@lru_cache
def get_reservation_service():
    return ReservationService()


class ReservationService:
    async def reserve_item(self, item: schemas.CartItem):
        # Call external service to reserve the item
        reservation_url = settings.reservation_url
        logger.debug(
            f"Reserving item: id={item.id} name={item.name} quantity={item.quantity}, reservation_url={reservation_url}"
        )

        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(
                    settings.reservation_url,
                    json={"id": item.id, "item": item.name, "quantity": item.quantity},
                )
                resp.raise_for_status()
            except httpx.HTTPStatusError as err:
                logger.error(
                    f"Got reservation error: id={item.id} name={item.name} details={str(err)}"
                )
                return
            except httpx.RequestError as err:
                logger.error(
                    f"Got network error: id={item.id} name={item.name} details={str(err)}"
                )
                return

        reservation_id = resp.json()["reservation_id"]
        logger.debug(f"Got reservation: id={reservation_id}")

        # Save the reservation ID to the item's DB record
        with models.get_db_session_ctx_mgr() as db:
            db_item = (
                db.query(models.CartItem).filter(models.CartItem.id == item.id).first()
            )
            db_item.reservation_id = reservation_id
            db.commit()
            db.refresh(db_item)
            logger.debug(
                f"Updated item reservation: id={item.id} reservation_id={reservation_id}"
            )
