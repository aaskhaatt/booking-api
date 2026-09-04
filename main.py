from routers.auth import router as auth_router
from routers.rooms import router as rooms_router
from routers.bookings import router as booking_router
from fastapi import FastAPI

app = FastAPI()


app.include_router(rooms_router)
app.include_router(auth_router)
app.include_router(booking_router)