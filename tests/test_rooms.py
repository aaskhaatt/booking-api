from main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_rooms(create_room):

    response = client.get("/rooms")

    assert response.status_code == 200

    rooms = response.json()

    assert len(rooms) == 1
    assert rooms[0]["number"] == 101
    assert rooms[0]["capacity"] == 2

def test_get_room_by_id(create_room):

    response = client.get(
        f"/rooms/{create_room.id}"
    )

    assert response.status_code == 200

    room = response.json()

    assert room["id"] == create_room.id
    assert room["number"] == 101


def test_get_room_not_found():

    response = client.get(
        "/rooms/999"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Room not found"