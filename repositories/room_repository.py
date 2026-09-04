from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Room
from exceptions import *



def get_room_by_id(room_id: int, db: Session):
    room = db.get(Room, room_id)

    if room is None:
        raise RoomNotFoundError()

    return room



def get_rooms(db: Session):
    stmt = select(Room)

    rooms = db.scalars(stmt).all()

    return rooms