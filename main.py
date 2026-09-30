from pydantic import BaseModel
from typing import List, Optional

class CartItem(BaseModel):
    name: str
    price: float

class CheckoutRequest(BaseModel):
    items: List[CartItem]
    utr_number: Optional[str] = None
    total_amount: Optional[float] = None

@app.post("/api/checkout")
async def checkout(payload: CheckoutRequest):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Store order along with UTR number in your database here
    # Example log: print(f"Received order with UTR: {payload.utr_number}")
    
    return {
        "status": "success",
        "message": "Order successfully submitted for payment verification!",
        "utr": payload.utr_number
    }
    
