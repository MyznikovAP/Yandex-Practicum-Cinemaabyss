from pydantic import BaseModel
from typing import Optional

class Payment(BaseModel):
    payment_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: float
    status: str
    timestamp: Optional[str] = None
    method_type: str