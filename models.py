from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProductDB(Base):  # like a JPA @Entity
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)  # auto-increments
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # exact money type, no float rounding
    quantity: Mapped[int]
