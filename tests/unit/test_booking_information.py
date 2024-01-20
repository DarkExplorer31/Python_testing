"""Booking information part unit tests"""
import pytest

from .test_authentication import client


@pytest.mark.parametrize(
    "competition_name,club_name",
    [
        ("Spring Festival", "Simply Lift"),
        ("Fall Classic", "Iron Temple"),
        ("Spring Festival", "She Lifts"),
    ],
)
def test_should_return_club_and_competition_with_200_status(
    client, competition_name, club_name
):
    response = client.get(f"/book/{competition_name}/{club_name}")
    assert response.status_code == 200


def test_should_return_to_welcome_page(client):
    response = client.get(f"/book/ExampleComp/ExampleClub")
    assert (
        b"Sorry, we could not find the requested information. Please try again."
        in response.data
    )
