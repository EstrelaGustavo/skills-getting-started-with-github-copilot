def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "description" in activities["Chess Club"]
    assert "participants" in activities["Chess Club"]


def test_signup_adds_participant(client):
    email = "new-student@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Student is already signed up for this activity"
    )
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert participants.count(email) == 1


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "new-student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_signup_removes_participant(client):
    email = "michael@mergington.edu"

    response = client.delete(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_remove_signup_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_signup_rejects_unregistered_participant(client):
    email = "not-registered@mergington.edu"

    response = client.delete(
        "/activities/Chess Club/signup", params={"email": email}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == (
        "Student is not signed up for this activity"
    )