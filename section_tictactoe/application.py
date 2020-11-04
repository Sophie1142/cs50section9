from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

# For more info:
# https://pythonhow.com/how-a-flask-app-works/
# https://www.freecodecamp.org/news/whats-in-a-python-s-name-506262fe61e8/
app = Flask(__name__)

# Configure session parameters
# https://flask-session.readthedocs.io/en/latest/
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Store board size
BOARD_SIZE = 3

@app.route("/")
def index():
    # For learning purposes
    print(__name__)

    # Set up 'board' in session to store player moves
    if "board" not in session:
        session["board"] = [[None, None, None],
                            [None, None, None],
                            [None, None, None]]

    # Set up 'turn' to store current player ('X' or 'O')
    if "turn" not in session:
        session["turn"] = "X"

    # Set up 'history' of moves in session
    if "history" not in session:
        session["history"] = []

    # Winner variable so we call render_template only once
    winner = None

    # Check for horizontal win (hint: consider using set() function)
    for i in range(BOARD_SIZE):
        if session["board"][i][0] != None and (len(set(session["board"][i])) == 1):
            winner=session["board"][i][0]

    # Check for column win
    for i in range(BOARD_SIZE):
        if session["board"][0][i] != None and len(set((session["board"][0][i],
                                                       session["board"][1][i],
                                                       session["board"][2][i]))) == 1 :
            winner=session["board"][0][i]

    # Check for left diagonal win
    if session["board"][0][0] != None and len(set([session["board"][0][0],
                                                   session["board"][1][1],
                                                   session["board"][2][2]])) == 1:
        winner=session["board"][0][i]

    # Check for right diagonal win
    if session["board"][0][2] != None and len(set([session["board"][0][2],
                                                   session["board"][1][1],
                                                   session["board"][2][0]])) == 1:
        winner = session['board'][0][2]

    # Announce winner if one exists
    if winner:
        return render_template("game.html", winner=winner)

    # Error check
    for move in session["board"]:
        print(*move)

    # Modify this function call to pass in needed parameters
    return render_template("game.html")

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

    # Capture who just played (X or o)
    session["board"][row][col]= session["turn"]

    # Add move to history
    session["history"] += [[session['turn'], row, col]]

    # Error check
    for move in session["history"]:
        print(*move)

    # Alternate turns
    if session["turn"] == "X":
        session["turn"] = "O"

    elif session["turn"] == "O":
        session["turn"] = "X"

    # Could also just use return redirect (as I do below), but wanted to show another example of url_for
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    # Delete all the session variables
    # (a for loop throws an error that size of dictionary
    # changed during iteration, so we'll go with this for now)
    del session["board"]
    del session["turn"]
    del session["history"]


    return redirect("/")

@app.route("/undo")
def undo():
    # delete from session board the last move played (aka session board index)
    if session['history'] == []:
        return render_template("game.html", error = "Sorry, there are no moves to undo")

    else:
        # Delete X or 0 from that grid cell
        session["board"][session['history'][-1][1]][session['history'][-1][2]] = None
        # Reset the turn
        session["turn"] = session["history"][-1][0]
        # Delete un-done move from session history
        del session["history"][-1]

    return redirect("/")
