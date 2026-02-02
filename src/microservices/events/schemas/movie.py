from pydantic import BaseModel
from typing import Optional

class Movie(BaseModel):
    movie_id: Optional[int] = None
    title: str
    action: str
    user_id: Optional[int] = None