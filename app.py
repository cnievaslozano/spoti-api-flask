import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# KEYS
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
app.secret_key = os.urandom(24)

scope = "user-library-read user-top-read"

sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope)




@app.route("/")
def index():
    return "¡Bienvenido! <a href='/login'>Iniciar sesión con Spotify</a>"

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect(url_for("top_tracks"))

@app.route("/top_tracks")
def top_tracks():
    token_info = session.get("token_info", None)
    if not token_info:
        return redirect(url_for("login"))

    sp = Spotify(auth=token_info["access_token"])
    top_tracks = sp.current_user_top_tracks(time_range="short_term", limit=5)

    return render_template("top-tracks.html", top_tracks=top_tracks)

if __name__ == "__main__":
    app.run(debug=True)
