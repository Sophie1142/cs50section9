from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# TODO: Configure session parameters


# Store board size
BOARD_SIZE = 3

@app.route("/")
def index():

    # Set up 'board' in session to store player moves

    # Set up 'turn' to store current player ('X' or 'O')

    # Set up 'history' of moves in session ()


    # Check for horizontal win (hint: consider using set() function)

    # Check for column win


    # Don't worry about horizontal wins for now

    # Error check
    for move in session["board"]:
        print(*move)

    # Modify this function call to pass in needed parameters
    return render_template("game.html")

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # Capture who just played


    # Add move to history


    # Error check
    for move in session["history"]:
        print(*move)

    # Alternate turns


    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    # session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
    if "board" in session:
        del session["board"]
    session["turn"] = "X"
    session["history"] = []

    return redirect("/")

@app.route("/undo")
def undo():
    # delete from session board the last move played (aka session board index)
    # session board index = history[-1]
    if session['history'] == []:
        return render_template("game.html", error = "Sorry, there are no moves to undo", game=session["board"], turn=session["turn"])

    else:
        # Delete X or 0 from that grid cell
        session["board"][session['history'][-1][1]][session['history'][-1][2]] = None
        # Reset the turn
        session["turn"] = session["history"][-1][0]
        # Delete un-done move from session history
        del session["history"][-1]

    return redirect("/")
