from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Product(Base):
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(50))
    price: Mapped[str] = mapped_column(String(50))
