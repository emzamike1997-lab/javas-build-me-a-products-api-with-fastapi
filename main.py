import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="build me a products API with FastAPI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Product(BaseModel):
    id: int
    name: str
    price: float

products = [
    Product(id=1, name="Product 1", price=10.99),
    Product(id=2, name="Product 2", price=9.99),
    Product(id=3, name="Product 3", price=12.99),
]

@app.get("/")
def root(): return {"status": "ok", "service": "build me a products API with FastAPI"}

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/products")
def get_products(): return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    return {"error": "Product not found"}

@app.post("/products")
def create_product(product: Product):
    products.append(product)
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    for i, p in enumerate(products):
        if p.id == product_id:
            products[i] = product
            return product
    return {"error": "Product not found"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for i, p in enumerate(products):
        if p.id == product_id:
            del products[i]
            return {"message": "Product deleted"}
    return {"error": "Product not found"}

if __name__ == "__main__":
    print("🚀 FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)