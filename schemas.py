from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    capacity: int
    

class BookingCreate(BaseModel):
    room_id: int 
    start_time: datetime
    end_time: datetime

class BookingUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None

class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    room_id: int
    start_time: datetime
    end_time: datetime
    created_at: datetime


class TokenResponse(BaseModel):
    message: str