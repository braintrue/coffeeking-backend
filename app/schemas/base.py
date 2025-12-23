from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True


class MenuCreate(MenuBase):
    pass


class MenuOut(MenuBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TableCreate(BaseModel):
    name: str
    capacity: int = 2
    tagline: Optional[str] = None
    location_code: str


class TableOut(BaseModel):
    id: int
    name: str
    capacity: int
    tagline: Optional[str] = None
    location_code: str
    current_count: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    table_id: int
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    created_at: datetime
    table_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class MatchCreate(BaseModel):
    host_id: int
    table_id: int


class MatchOut(BaseModel):
    id: int
    host_id: int
    guest_id: Optional[int] = None
    table_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
