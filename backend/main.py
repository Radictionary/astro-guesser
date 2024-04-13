from flask import Flask, send_from_directory

app = Flask(__name__)


# Routes
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/content")
def content():
    return "hi"

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
    app.run("0.0.0.0", 8080, debug=True)
