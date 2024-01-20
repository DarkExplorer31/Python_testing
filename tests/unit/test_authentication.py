"""Authentication unit tests"""
import pytest

import server
from server import app, loadClubs


@pytest.fixture
def client():
    """Create a test client for the app."""
    return app.test_client()


# loadClubs testing part
def test_should_import_clubs():
    clubs = loadClubs()
    expected_value = {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
    }
    assert clubs == expected_value["clubs"]


def test_should_return_value_error(monkeypatch):
    def mockreturn():
        return {
            "key": [
                {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
                {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
                {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
            ]
        }

    clubs = monkeypatch.setattr(server, "loadClubs", mockreturn)
    expected_value = {
        "clubs": [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]
    }
    assert clubs != expected_value["clubs"]


def test_should_return_none():
    clubs = loadClubs("not_exists.json")
    assert clubs is None


# authentication part
def test_index_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_show_summary_should_connected(client):
    email = "john@simplylift.co"
    request = client.post("/showSummary", data={"email": email})
    assert request.status_code == 200


def test_show_summary_should_return_not_found_error(client):
    email = "test@test.co"
    request = client.post("/showSummary", data={"email": email})
    data = request.data.decode()
    assert request.status_code == 404
    assert data.find("<h1>Error 404</h1>") != -1
    assert data.find("Your email does not exist in our database.")


def test_show_summary_without_email_should_return_405(client):
    response = client.get("/showSummary")
    data = response.data.decode()
    assert response.status_code == 405
    assert data.find("<h1>Error 405</h1>") != -1


def test_should_logout(client):
    email = "john@simplylift.co"
    request = client.post("/showSummary", data={"email": email})
    assert request.status_code == 200
    logout = client.get("/logout", follow_redirects=True)
    assert logout.status_code == 200
