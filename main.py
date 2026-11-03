from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import RedirectResponse
from models import ProductDB
from schemas import Product,ProductCreate
from database import Base, engine, get_db

app = FastAPI() # need to have fastapi obj so that we are telling fastapi that this is a fastapi app

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],  # allow all headers
)

Base.metadata.create_all(bind=engine)  # creates tables that don't exist yet

@app.get("/")
def greet():
    return "Hello, World!"  

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(ProductDB).all()
    return products

@app.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_db = ProductDB(**product.model_dump())  # convert ProductCreate to ProductDB
    db.add(product_db)
    db.commit()
    db.refresh(product_db)  # get the auto-generated id
    return product_db

@app.get("/products/{product_id}",response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return None
    return product

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return RedirectResponse(url="/products", status_code=303)

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    product_db = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product_db:
        return None
    for key, value in product.model_dump().items():
        setattr(product_db, key, value)
    db.commit()
    db.refresh(product_db)
    return product_db