from fastapi import FastAPI, Request, Depends, HTTPException, Form, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from database import init_db, SessionLocal, ProductModel, UserModel, OrderModel

app = FastAPI(title="Glassmorphism Dressing E-Commerce")

init_db()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session):
    username = request.cookies.get("user")
    if not username:
        return None
    return db.query(UserModel).filter(UserModel.username == username).first()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(ProductModel).all()
    user = get_current_user(request, db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "user": user
    })

@app.post("/api/register")
async def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.username == username).first()
    if existing:
        return JSONResponse({"status": "error", "message": "Username already taken"}, status_code=400)
    
    hashed = UserModel.get_password_hash(password)
    new_user = UserModel(username=username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    
    response = JSONResponse({"status": "success", "message": "User registered successfully!"})
    response.set_cookie(key="user", value=username)
    return response

@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not user.verify_password(password):
        return JSONResponse({"status": "error", "message": "Invalid username or password"}, status_code=400)
    
    response = JSONResponse({"status": "success", "message": "Logged in successfully!"})
    response.set_cookie(key="user", value=username)
    return response

@app.post("/api/logout")
async def logout():
    response = JSONResponse({"status": "success", "message": "Logged out"})
    response.delete_cookie("user")
    return response

@app.post("/api/checkout")
async def checkout(order_data: dict, request: Request, db: Session = Depends(get_db)):
    items = order_data.get("items", [])
    if not items:
        return {"status": "error", "message": "Cart is empty"}
    
    user = get_current_user(request, db)
    total = sum(item["price"] for item in items)
    items_summary = ", ".join(item["name"] for item in items)
    
    new_order = OrderModel(
        user_id=user.id if user else None,
        total_amount=total,
        items_summary=items_summary
    )
    db.add(new_order)
    db.commit()
    
    return {"status": "success", "message": f"Order placed successfully for ${total:.2f}!"}

@app.get("/api/orders")
async def get_orders(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return JSONResponse({"status": "error", "message": "Please log in to view orders"}, status_code=401)
    
    orders = db.query(OrderModel).filter(OrderModel.user_id == user.id).all()
    return {
        "status": "success",
        "orders": [
            {
                "id": o.id,
                "items": o.items_summary,
                "total": o.total_amount,
                "date": o.created_at.strftime("%Y-%m-%d %H:%M")
            } for o in orders
        ]
    }
  
