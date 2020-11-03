from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# TODO: Configure session parameters
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# Store board size
BOARD_SIZE = 3

@app.route("/")
def index():

    # Set up 'board' in session to store player moves
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]

    # Set up 'turn' to store current player ('X' or 'O')
    if "turn" not in session:
        session["turn"] = "X"

    # Set up 'history' of moves in session ()
    if "history" not in session:
        session["history"] = []


    # Check for horizontal win (hint: consider using set() function)
    for i in range(BOARD_SIZE):
        if (len(set(session["board"][i])) == 1) and session["board"][i][0] != None:
            # Announce winner
            return render_template("game.html", winner=session["board"][i][0])

    # Check for column win
    for i in range(BOARD_SIZE):
        if len(set((session["board"][0][i], session["board"][1][i], session["board"][2][i]))) == 1 and session["board"][0][i] != None:
            # Announce winner
            return render_template("game.html", winner=session["board"][0][i])

    # Check for column win


    # Don't worry about horizontal wins for now

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
