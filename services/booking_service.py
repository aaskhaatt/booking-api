from repositories.room_repository import get_room_by_id
from repositories.booking_repository import (
    get_conflicting_bookings,
    create_booking,
    get_user_bookings,
    get_booking_by_id,
    delete_booking,
    update_booking
)
from exceptions import *



def create_booking_service(user_id: int, booking_data, db):
    
    if booking_data.start_time >= booking_data.end_time:
        raise InvalidBookingTimeError()
    
    get_room_by_id(booking_data.room_id, db)

    bookings = get_conflicting_bookings(booking_data.room_id, booking_data.start_time, booking_data.end_time, db)

    if bookings:
        raise BookingConflictError()

    return create_booking(user_id, booking_data.room_id, booking_data.start_time, booking_data.end_time, db)



def get_user_bookings_service(user_id, db):

    return get_user_bookings(user_id, db)


def delete_booking_service(booking_id, user_id, db):
    booking = get_booking_by_id(booking_id, db)

    if booking.user_id != user_id:
        raise BookingAccessDeniedError()

    delete_booking(booking, db)



def update_booking_service(booking_id, user_id, booking_data, db):
    booking = get_booking_by_id(booking_id, db)

    if booking.user_id != user_id:
        raise BookingAccessDeniedError()

    start_time = booking_data.start_time if booking_data.start_time is not None else booking.start_time

    end_time = booking_data.end_time if booking_data.end_time is not None else booking.end_time
    
    if start_time >= end_time:
         raise InvalidBookingTimeError()


    conflicts = get_conflicting_bookings(booking.room_id, start_time, end_time, db, booking_id)

    if conflicts:
        raise BookingConflictError()
    
    return update_booking(booking, start_time, end_time, db)


def get_booking_service(booking_id, user_id, db):
    booking = get_booking_by_id(booking_id, db)
     
    if booking.user_id != user_id:
        raise BookingAccessDeniedError()
     
    return booking