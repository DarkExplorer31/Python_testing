"""Integration tests"""
import pytest

from server import app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    """Create a test client for the app."""
    return app.test_client()


def test_should_purchase_one_place_by_club(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "1",
        },
    )
    request2 = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[1]["name"],
            "places": "1",
        },
    )
    request3 = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[2]["name"],
            "places": "1",
        },
    )
    response = client.get(f"/book/Spring Festival/Iron Temple")
    assert request.status_code == 200
    assert b"Welcome, john@simplylift.co" in request.data
    assert (
        b"Competition has 24 places left and you have 12 points left." in request.data
    )
    assert request2.status_code == 200
    assert b"Welcome, admin@irontemple.com" in request2.data
    assert (
        b"Competition has 23 places left and you have 3 points left." in request2.data
    )
    assert request3.status_code == 200
    assert b"Welcome, kate@shelifts.co.uk" in request3.data
    assert (
        b"Competition has 22 places left and you have 11 points left." in request3.data
    )
    assert response.status_code == 200
    assert b"Places available: 22" in response.data
