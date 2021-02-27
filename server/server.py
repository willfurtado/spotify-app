from flask import Flask, redirect, request, render_template
from playlist_generator import playlistGenerator

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/', methods=['POST','GET'])
def home_post():
    text = request.form['text']
    playlistGenerator(text)
    return render_template("success.html")


if __name__ == "__main__":
	app.run(debug=True)