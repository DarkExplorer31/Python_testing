import json
import os
from flask import Flask, render_template, request, redirect, flash, url_for, abort


def loadClubs(clubs_path="clubs.json"):
    if os.path.exists(clubs_path):
        with open(clubs_path) as c:
            listOfClubs = json.load(c)["clubs"]
            return listOfClubs
    else:
        return None


def loadCompetitions(listOfCompetitions_path="competitions.json"):
    if os.path.exists(listOfCompetitions_path):
        with open(listOfCompetitions_path) as comps:
            listOfCompetitions = json.load(comps)["competitions"]
            return listOfCompetitions
    else:
        return None


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        abort(404)
        flash("Your email does not exist in our database.")
    clubPoint = int(club["points"])
    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        clubPoint=clubPoint,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(405)
def not_ability_error(error):
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run(debug=True)
