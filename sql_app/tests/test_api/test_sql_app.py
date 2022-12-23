from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={"email": "deadpool@example.com", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["id"] == user_id


def test_get_one_user(client, db, fill_db_with_data):
    '''Check '''
    db_user = [*fill_db_with_data]
    response = client.get(f"/users/{db_user[0].id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@email"
    assert data["id"] == db_user[0].id
    assert len(data["items"]) == 2

    # Проверяем каждое поле отдельно
    assert data["items"][0]["title"] == "test_title_1_user_1"
    assert data["items"][0]["description"] == "test_description_1_user_1"
    assert data["items"][0]["owner_id"] == db_user[0].id
    assert data["items"][1]["title"] == "test_title_2_user_1"
    assert data["items"][1]["description"] == "test_description_2_user_1"
    assert data["items"][1]["owner_id"] == db_user[0].id


def test_get_user_with_invalid_id(db: Session, client: TestClient):
    response = client.get(f"/users/{0}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "User does not exists"