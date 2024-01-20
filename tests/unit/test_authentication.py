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
