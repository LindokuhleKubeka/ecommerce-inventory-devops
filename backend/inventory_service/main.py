from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
async def get_products():
    return [{"name": "Laptop", "price": 999.99, "quantity": 10}]

@app.get("/")
async def root():
    return {"message": "Inventory Service is running"}
