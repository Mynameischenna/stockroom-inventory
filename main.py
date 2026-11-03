from fastapi import Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import ProductDB
from schemas import Product, ProductCreate

app = FastAPI(title="Stockroom Inventory API")  # need to have fastapi obj so that we are telling fastapi that this is a fastapi app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

Base.metadata.create_all(bind=engine)  # creates tables that don't exist yet


def get_product_or_404(product_id: int, db: Session) -> ProductDB:
    product = db.get(ProductDB, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.get("/")
def greet():
    return "Hello, World!"


@app.get("/products", response_model=list[Product])
def get_all_products(db: Session = Depends(get_db)):
    return db.scalars(select(ProductDB).order_by(ProductDB.id)).all()


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_db = ProductDB(**product.model_dump())  # convert ProductCreate to ProductDB
    db.add(product_db)
    db.commit()
    db.refresh(product_db)  # get the auto-generated id
    return product_db


@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return get_product_or_404(product_id, db)


@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    product_db = get_product_or_404(product_id, db)
    for key, value in product.model_dump().items():
        setattr(product_db, key, value)
    db.commit()
    db.refresh(product_db)
    return product_db


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_db = get_product_or_404(product_id, db)
    db.delete(product_db)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
