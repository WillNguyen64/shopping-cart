from sqlalchemy import Column, Integer, String

from .database import Base


class CartItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer)
    reservation_id = Column(Integer)
