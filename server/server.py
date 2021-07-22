from flask import Flask, request, render_template
from playlist_generator import generate_playlist

scope = "playlist-modify-public ugc-image-upload"

app = Flask(__name__)

app.secret_key = "OskiOski1868"
app.config["SESSION_COOKIE_NAME"] = "spotify-login-session"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
def home_post():
    text = request.form["text"]
    url = generate_playlist(text)
    return render_template("success.html", url=url)


if __name__ == "__main__":
    app.run(debug=True)
