"""Booking information part unit tests"""
from .test_authentication import client


def test_should_return_table(client):
    response = client.get("/pointsDisplay")
    assert response.status_code == 200
    data = response.data.decode()
    assert data.find("<td>Simply Lift</td>")
    assert data.find("<td>13</td>")
    assert data.find("<td>She Lifts</td>")
    assert data.find("<td>12</td>")
