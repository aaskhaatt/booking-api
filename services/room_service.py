from repositories.room_repository import *


def get_rooms_service(db):
    return get_rooms(db)

def get_room_service(room_id, db):
    return get_room_by_id(room_id, db)