from routers.auth import router as auth_router
from routers.rooms import router as rooms_router
from routers.bookings import router as booking_router
from fastapi import FastAPI
from handlers import exception_handler, ERROR_RESPONSES
from exceptions import *

app = FastAPI()
for error in ERROR_RESPONSES:
    app.add_exception_handler(error, exception_handler)

app.include_router(rooms_router)
app.include_router(auth_router)
app.include_router(booking_router)