from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database connection
DATABASE_URL = "postgresql://postgres:password@localhost:5433/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Inventory Service is running"}

@app.get("/products")
async def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.post("/products")
async def add_product(name: str, price: float, quantity: int):
    db = SessionLocal()
    product = Product(name=name, price=price, quantity=quantity)
    db.add(product)
    db.commit()
    db.refresh(product)
    db.close()
    return {"message": "Product added", "product": {"id": product.id, "name": product.name, "price": product.price, "quantity": product.quantity}}
