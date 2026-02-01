from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: Optional[int] = None
    username: str
    action: str
    timestamp: Optional[str] = None