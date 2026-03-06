from fastapi.testclient import TestClient

from src import app

client = TestClient(app.app)


def test_signup_and_remove():
    # ensure initial state
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    assert "Chess Club" in activities

    # sign up a new student
    email = "test@mergington.edu"
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200
    # refetch to confirm
    resp = client.get("/activities")
    activities = resp.json()
    assert email in activities["Chess Club"]["participants"]

    # cannot sign up twice
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 400

    # remove the student
    resp = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp.status_code == 200
    resp = client.get("/activities")
    activities = resp.json()
    assert email not in activities["Chess Club"]["participants"]

    # removing non-existent participant returns 404
    resp = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp.status_code == 404
