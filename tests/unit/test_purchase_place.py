"""Purchase places part unit tests"""
import pytest

import server
from .test_authentication import client
from server import loadCompetitions, loadClubs


@pytest.fixture
def client_mocker(client, mocker):
    mocker.patch.object(
        server, "competitions", [{"name": "ExampleCompetition", "numberOfPlaces": 5}]
    )
    mocker.patch.object(server, "clubs", [{"name": "ExampleClub", "points": 20}])
    yield client


# loadCompetitions part
def test_should_import_list_of_competition():
    listOfCompetitions = loadCompetitions()
    expected_value = {
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]
    }
    assert listOfCompetitions == expected_value["competitions"]


def test_should_return_list_of_competition(client):
    email = "john@simplylift.co"
    request = client.post("/showSummary", data={"email": email})
    data = request.data.decode()
    assert data.find("Spring Festival")
    assert data.find("Fall Classic")


def test_should_return_clubs_at_start(client):
    email = "john@simplylift.co"
    request = client.post("/showSummary", data={"email": email})
    data = request.data.decode()
    assert data.find("<h2>Welcome, john@simplylift.co </h2>") != -1
    assert data.find("Points available: 12") != -1


def test_should_return_None_to_competitions():
    competitions = loadCompetitions("not_exist.json")
    assert competitions is None


# purchasePlaces part
def test_should_reserve_a_place_in_flash(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "2",
        },
    )
    data = request.data.decode()
    assert request.status_code == 200
    assert (
        data.find(
            "<li>Competition has 20 places left and you have 10 points left.</li>"
        )
        != -1
    )


def test_should_return_400_with_under_one_flash(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "-2",
        },
    )
    data = request.data.decode()
    assert request.status_code == 400
    assert data.find("You can't reserve a spot below 1.")


def test_should_return_400_with_not_enough_points_flash(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "56",
        },
    )
    data = request.data.decode()
    assert request.status_code == 400
    assert data.find("Not enough points.")


def test_should_return_current_number_of_places_from_competition(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "2",
        },
    )
    request2 = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "2",
        },
    )
    data = request2.data.decode()
    assert request.status_code == 200
    assert request2.status_code == 200
    assert data.find("Number of Places: 21")


def test_should_return_current_number_of_points(client):
    clubs = loadClubs()
    competitions = loadCompetitions()
    request = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "2",
        },
    )
    request2 = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": "2",
        },
    )
    data = request2.data.decode()
    assert request.status_code == 200
    assert request2.status_code == 200
    assert data.find("Points available: 2") != -1


def test_should_return_competition_is_complete(client_mocker):
    data = {
        "competition": "ExampleCompetition",
        "club": "ExampleClub",
        "places": 5,
    }
    response = client_mocker.post("/purchasePlaces", data=data)
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
