from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from datetime import date

class Item(BaseModel):
    _id: int
    name: str
    description: Optional[str] = None
    price: float
    date_: date = None
    working : List = None

class UserCreate(BaseModel):
    _id: str
    name: str
    age: int
    email: str
    company_name: str
    date_:date = None

class User(UserCreate):
    id: str  # MongoDB uses ObjectId, but we'll represent it as a string

    class Config:
        from_attributes = True

class StatusChoice(str, Enum):
    pending = "Pending"
    inprogress = "Inprogress"
    completed = "Completed"

class TodoCreate(BaseModel):
    task: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: StatusChoice = StatusChoice.pending
    user_id: str  # Reference to User

class Todo(TodoCreate):
    id: str  # MongoDB uses ObjectId, but we'll represent it as a string
    created_at: datetime
    completed_date: Optional[datetime] = None

    class Config:
        from_attributes = True



