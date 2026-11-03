from pydantic import BaseModel, ConfigDict, Field

class ProductCreate(BaseModel):          # what the client sends (no id)
    name: str
    description: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

class Product(ProductCreate):            # what we send back (with id)
    id: int
    model_config = ConfigDict(from_attributes=True)  # lets Pydantic read a ProductDB object
