"""
    This is the main file of the game. It bootstrap the backend and begins a Flask server that
    serves content. It also sets up a SocketIO server that listens for incoming messages.

    The main components of the backend are:
    - Flask: A web server that serves the frontend and handles HTTP requests.
    - SocketIO: A protocol that allows for real-time communication between the client and the server.

"""

from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
import json
import data
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Random secret key -- upgrade for production
app.config['SECRET_KEY'] = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(50))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

# Routes
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")
@app.route("/game_selector")
def game_selector():
    return send_from_directory("../frontend", "game_selector.html")
@app.route("/ws_test")
def ws_test():
    return send_from_directory("../frontend", "ws_test.html")
@app.route("/login")
def login():
    return send_from_directory("../frontend", "login.html")
@app.route("/signup")
def signup():
    return send_from_directory("../frontend", "signup.html")
@app.route("/profile")
def profile():
    return "Profile"


# SocketIO events
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")
    return send_from_directory("../frontend", "index.html")

@socketio.on("message")
def handle_message(message):
    print("received message: " + message)
    emit("message", message)
    message = json.loads(message)
    match message["label"]:
        case "need_data":
            emit("message", json.dumps({"label": "question", "data": data.get_random_data()}))
        case "game_score":
            pass


# Static files
@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("../frontend/css", path)

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("../frontend/js", path)

@app.route("/img/<path:path>")
def send_img(path):
    return send_from_directory("../frontend/img", path)

@app.route("/fonts/<path:path>")
def send_font(path):
    return send_from_directory("../frontend/fonts", path)

if __name__ == "__main__":
    # run
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
