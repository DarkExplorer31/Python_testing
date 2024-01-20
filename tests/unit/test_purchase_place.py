"""Purchase places part unit tests"""
import server
from .test_authentication import client
from server import loadCompetitions


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
    assert data.find("Points available: 13") != -1


def test_should_return_None_to_competitions():
    competitions = loadCompetitions("not_exist.json")
    assert competitions is None
