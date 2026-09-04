from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Booking
from datetime import datetime
from exceptions import *



def get_booking_by_id(booking_id: int, db: Session):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise BookingNotFoundError()

    return booking


def get_user_bookings(user_id: int, db: Session):
    stmt = select(Booking).where(Booking.user_id == user_id)

    bookings = db.scalars(stmt).all()
    
    return bookings


def create_booking(user_id: int, room_id: int, start_time: datetime, end_time: datetime, db: Session):
    booking = Booking(
        user_id=user_id,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking

def get_conflicting_bookings(
    room_id: int,
    start_time: datetime,
    end_time: datetime,
    db: Session,
    exclude_booking_id: int | None = None
):
    
    stmt = select(Booking).where(Booking.room_id == room_id, Booking.start_time < end_time, Booking.end_time > start_time)

    if exclude_booking_id:
        stmt = stmt.where(Booking.id != exclude_booking_id)

    bookings = db.scalars(stmt).all()

    return bookings


def delete_booking(booking, db):
    db.delete(booking)
    db.commit()


def update_booking(booking: Booking,
                   start_time: datetime,
                   end_time: datetime,
                   db: Session):
    booking.start_time = start_time
    booking.end_time = end_time

    db.commit()
    db.refresh(booking)

    return booking
