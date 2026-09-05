import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import get_db, Base
from main import app


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


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db