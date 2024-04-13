from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Routes
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/socket")
def socket():
    return send_from_directory("../frontend", "socket.html")


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
    # app.run("0.0.0.0", 8080, debug=True)
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
