from database import SessionLocal
from models import Room

def seed_rooms():
    db = SessionLocal()

    rooms = [
        Room(
            number=101,
            capacity=2
        ),
        Room(
            number=102,
            capacity=4
        ),
        Room(
            number=103,
            capacity=6
        )
    ]

    db.add_all(rooms)
    db.commit()

    db.close()


if __name__ == "__main__":
    seed_rooms()
