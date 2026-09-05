from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import (
    UserNotFoundError,
    UserAlreadyExistsError,
    RoomNotFoundError,
    BookingNotFoundError,
    BookingConflictError,
    BookingAccessDeniedError,
    InvalidBookingTimeError
)

ERROR_RESPONSES = {
    UserNotFoundError: (404, "User Not Found"),
    RoomNotFoundError: (404, "Room not found"),
    BookingNotFoundError: (404, "Booking not found"),

    UserAlreadyExistsError: (409, "User already exists"),
    BookingConflictError: (409, "Booking conflict"),

    BookingAccessDeniedError: (403, "Access denied"),
    InvalidBookingTimeError: (400, "Invalid booking time"),
}


async def exception_handler(request: Request, exc):
    status_code, message = ERROR_RESPONSES[type(exc)]

    return JSONResponse(status_code=status_code, content = {"detail": message})
