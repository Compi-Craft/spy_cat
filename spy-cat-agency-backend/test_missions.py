import pytest
from fastapi.testclient import TestClient
from main import app  # імпортуй свій FastAPI app
from database import Base, engine, SessionLocal

# Підготуй базу для тестування
@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

# Тестові дані
spy_cat = {
    "name": "Whiskers",
    "years_experience": 3,
    "breed": "Siberian",
    "salary": 5000.0
}

targets = [
    {"name": "Target 1", "country": "USA", "notes": "Secret files"},
    {"name": "Target 2", "country": "Germany"},
    {"name": "Target 3", "country": "France", "notes": ""}
]

def test_create_spy_cat():
    response = client.post("/cats/", json=spy_cat)
    assert response.status_code == 201
    assert response.json()["name"] == spy_cat["name"]

def test_create_invalid_mission_too_many_targets():
    response = client.post("/missions/", json={
        "targets": targets + [{"name": "Too much", "country": "UK"}]
    })
    assert response.status_code == 400
    assert "1 to 3 targets" in response.json()["detail"]

def test_create_valid_mission():
    response = client.post("/missions/", json={"targets": targets})
    assert response.status_code == 201
    assert response.json()["completed"] is False
    global mission_id, target_ids
    mission_id = response.json()["id"]
    target_ids = [t["id"] for t in response.json()["targets"]]

def test_assign_cat_to_mission():
    # Get first cat
    cats = client.get("/cats/").json()
    cat_id = cats[0]["id"]
    # Assign to mission
    response = client.put(f"/missions/{mission_id}/assign_cat?cat_id={cat_id}")
    assert response.status_code == 200
    assert "assigned" in response.json()["detail"]

def test_prevent_double_assign():
    cats = client.get("/cats/").json()
    cat_id = cats[0]["id"]
    # Try assign again
    response = client.put(f"/missions/{mission_id}/assign_cat?cat_id={cat_id}")
    assert response.status_code == 400
    assert "Mission already assigned to a cat" in response.json()["detail"]

def test_update_notes():
    response = client.put(
        f"/missions/targets/{target_ids[0]}/notes",
        params={"notes": "Updated notes"}
    )
    assert response.status_code == 200
    assert response.json()["notes"] == "Updated notes"

def test_complete_target_and_mission():
    for tid in target_ids:
        res = client.put(f"/missions/targets/{tid}/complete")
        assert res.status_code == 200
        assert res.json()["completed"] is True

    # Перевіримо, що місія тепер завершена
    res = client.get(f"/missions/{mission_id}")
    assert res.status_code == 200
    assert res.json()["completed"] is True

def test_list_missions():
    res = client.get("/missions/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
