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


def initializePlacesBuying():
    placesBuy = {}
    for club in clubs:
        pointsByCompetitions = [
            {competition["name"]: 0} for competition in competitions
        ]
        placesBuy[club["name"]] = pointsByCompetitions
    return placesBuy


places_buy_list = initializePlacesBuying()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Your email does not exist in our database.")
        abort(404)
    clubPoint = int(club["points"])
    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        clubPoint=clubPoint,
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Sorry, we could not find the requested information. Please try again.")
        return render_template("welcome.html", club=club, competitions=competitions)
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    clubPoint = int(club["points"])
    placesRequired = int(request.form["places"])
    competitionPlaces = int(competition["numberOfPlaces"])
    if placesRequired < 1:
        flash("You can't reserve a place below 1.")
        abort(400)
    elif (
        placesRequired > clubPoint
        or placesRequired > competitionPlaces
        or placesRequired > 12
    ):
        flash("Not enough points.")
        abort(400)
    else:
        clubPoint -= placesRequired
        competitionPlaces = int(competitionPlaces) - placesRequired
        competition["numberOfPlaces"] = str(competitionPlaces)
        club["points"] = str(clubPoint)
        clubTotalPoint = places_buy_list[club["name"]]
        for competitionName in clubTotalPoint:
            if competition["name"] in competitionName:
                competitionName[competition["name"]] += placesRequired
                if competitionName[competition["name"]] > 12:
                    flash(f"You have used too many points in {competition['name']}.")
                    abort(400)
    if competitionPlaces == 0:
        flash("Great-booking complete!")
    else:
        flash(
            f"Competition has {competitionPlaces} places left and you have {clubPoint} points left."
        )
    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        clubPoint=clubPoint,
    )


@app.route("/pointsDisplay", methods=["GET"])
def pointsDisplay():
    return render_template("points.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


@app.errorhandler(400)
def not_ability_error(error):
    return render_template("400.html"), 400


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(405)
def not_ability_error(error):
    return render_template("405.html"), 405


if __name__ == "__main__":
    app.run(debug=True)
