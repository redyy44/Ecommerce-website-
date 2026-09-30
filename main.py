from fastapi import FastAPI, Request, Form, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI()

# Mount static directory for CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Mock product catalog
PRODUCTS = [
    {"name": "Floral Maxi Dress", "price": 99.00, "image": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?auto=format&fit=crop&w=500&q=80"},
    {"name": "Silky Slip Dress", "price": 85.00, "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=500&q=80"},
    {"name": "Elegant Gown", "price": 149.00, "image": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?auto=format&fit=crop&w=500&q=80"},
    {"name": "Ethereal Sundress", "price": 79.00, "image": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=500&q=80"},
    {"name": "Linen Dress", "price": 110.00, "image": "https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=500&q=80"},
    {"name": "Velvet Evening Dress", "price": 185.00, "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=500&q=80"}
]

class CartItem(BaseModel):
    name: str
    price: float

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    utr_number: Optional[str] = None
    total_amount: Optional[float] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "products": PRODUCTS, "user": None})

@app.post("/api/checkout")
async def checkout(payload: CheckoutRequest):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return {
        "status": "success",
        "message": "Order placed successfully!",
        "utr": payload.utr_number
    }

@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"status": "success", "message": f"Welcome back, {username}!"}

@app.post("/api/register")
async def register(username: str = Form(...), password: str = Form(...)):
    return {"status": "success", "message": "Account created successfully!"}

@app.post("/api/logout")
async def logout():
    return {"status": "success", "message": "Logged out successfully"}
    
