from typing import List, Optional, Union
from typing_extensions import Annotated

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator


def name_not_empty(value: str):
    assert value not in (None, ""), "Name must not be empty"
    return value


def quantity_between_1_and_100(value: int):
    assert 1 <= value <= 100, "Quantity must be between 1 and 100"
    return value


ItemName = Annotated[str, AfterValidator(name_not_empty)]
ItemQuantity = Annotated[
    int,
    AfterValidator(quantity_between_1_and_100),
]


class CartItemBase(BaseModel):
    name: ItemName
    quantity: Optional[ItemQuantity] = 1


class CartItemCreate(CartItemBase):
    class Config:
        json_schema_extra = {"examples": [{"name": "item1", "quantity": 5}]}


class CartItem(CartItemBase):
    id: int
    reservation_id: Union[int, None] = None

    class Config:
        json_schema_extra = {
            "examples": [
                {"id": 1, "name": "item1", "quantity": 5, "reservation_id": 1001}
            ]
        }
        orm_mode = True


class CartItemList(BaseModel):
    items: List[CartItem]
