from datetime import datetime

from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_create_booking(client, auth_headers, create_room):

    response = client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T12:00:00"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["room_id"] == create_room.id
    assert data["start_time"].startswith("2026-09-10")



def test_get_my_bookings(client, auth_headers, create_room):

    client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T12:00:00"
        }
    )

    response = client.get(
        "/bookings",
        headers=auth_headers
    )

    assert response.status_code == 200

    bookings = response.json()

    assert len(bookings) == 1
    assert bookings[0]["room_id"] == create_room.id



def test_get_booking_by_id(client, auth_headers, create_room):

    create_response = client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T12:00:00"
        }
    )

    booking_id = create_response.json()["id"]

    response = client.get(
        f"/bookings/{booking_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == booking_id


def test_cannot_get_other_user_booking(client, auth_headers, create_room, create_user):

    # создаём бронь первым пользователем
    booking_response = client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T12:00:00"
        }
    )

    booking_id = booking_response.json()["id"]


    # создаём второго пользователя
    second_user_response = client.post(
        "/auth/register",
        json={
            "username": "second",
            "email": "second@test.com",
            "password": "123456"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "second@test.com",
            "password": "123456"
        }
    )

    second_token = login_response.json()["access_token"]

    second_headers = {
        "Authorization": f"Bearer {second_token}"
    }


    # второй пользователь пытается получить чужую бронь
    response = client.get(
        f"/bookings/{booking_id}",
        headers=second_headers
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Access denied"



def test_booking_conflict(client, auth_headers, create_room):

    first_response = client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T10:00:00",
            "end_time": "2026-09-10T12:00:00"
        }
    )

    assert first_response.status_code == 200


    second_response = client.post(
        "/bookings",
        headers=auth_headers,
        json={
            "room_id": create_room.id,
            "start_time": "2026-09-10T11:00:00",
            "end_time": "2026-09-10T13:00:00"
        }
    )


    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Booking conflict"