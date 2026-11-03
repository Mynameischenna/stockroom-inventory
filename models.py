from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProductDB(Base):  # like a JPA @Entity
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)  # auto-increments
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    price: Mapped[float]
    quantity: Mapped[int]
