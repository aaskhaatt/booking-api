from fastapi import APIRouter, Depends
from services.room_services import * 
from database import get_db
from schemas import RoomResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=list[RoomResponse])
def get_rooms(db: Session = Depends(get_db)):
    return get_rooms_service(db)

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    return get_room_service(room_id, db)