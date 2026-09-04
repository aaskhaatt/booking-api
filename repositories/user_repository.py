from sqlalchemy.orm import Session
from models import User
from exceptions import *
from sqlalchemy import select



def get_user_by_id(user_id: int, db: Session):
    user = db.get(User, user_id)

    if user is None:
        raise UserNotFoundError()

    return user



def create_user(username: str, email: str, password_hash: str, db: Session):
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(email: str, db: Session):
    stmt = select(User).where(User.email == email)

    user = db.scalars(stmt).first()

    if user is None:
        raise UserNotFoundError()

    return user