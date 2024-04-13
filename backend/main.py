from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "hi!!!"

if __name__ == "__main__":
    app.run("0.0.0.0", 8080)