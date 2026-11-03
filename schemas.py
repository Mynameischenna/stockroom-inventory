from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):          # what the client sends (no id)
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=500)
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    quantity: int = Field(ge=0)


class Product(ProductCreate):            # what we send back (with id)
    id: int
    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read a ProductDB object
