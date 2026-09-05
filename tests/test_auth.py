from fastapi.testclient import TestClient
from main import app
import pytest
from database import Base

client = TestClient(app)



def test_register_user():
    response = client.post(
        "/auth/register", 
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "qwerty"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@email.com"


def test_register_duplicate_email():
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "test@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "User already exists"



def test_login_success():
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@email.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@email.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"