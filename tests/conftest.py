import pytest
from models import Room, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.user_service import hash_password
from database import get_db, Base
from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)

TEST_DATABASE_URL = (
    "postgresql://postgres:password@localhost/booking_test"
)

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(bind=engine, 
                                   autocommit=False, 
                                   autoflush=False)


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)




@pytest.fixture
def auth_headers(client, create_user):

    response = client.post(
        "/auth/login",
        json={
            "email": create_user.email,
            "password": "123456"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }



@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()



def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db



@pytest.fixture
def create_room(db_session):
    room = Room(
        number=101,
        capacity=2
    )

    db_session.add(room)
    db_session.commit()
    db_session.refresh(room)

    return room


@pytest.fixture
def create_user(db_session):
    user = User(
        username="testuser",
        email="test@email.com",
        password_hash=hash_password("123456")
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user