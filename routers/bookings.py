from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookingCreate, BookingResponse, BookingUpdate
from services.booking_service import *
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/bookings", tags=["bookings"])





@router.post("", response_model=BookingResponse)
def create_booking(booking: BookingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_booking_service(user_id=current_user.id, booking_data=booking, db=db)




@router.get("", response_model=list[BookingResponse])
def get_my_bookings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_bookings_service(user_id=current_user.id, db=db)



    
@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(booking_id: int, current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    return get_booking_service(booking_id, user_id=current_user.id, db=db)



@router.patch("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_booking_service(booking_id, user_id=current_user.id, booking_data=booking, db=db)




@router.delete("/{booking_id}")
def delete_booking(booking_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    delete_booking_service(booking_id, user_id=current_user.id, db=db)

    return {"message": "Booking deleted"}
    
    