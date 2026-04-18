from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Import your own files
from PlaylistDriver import get_playlists, createPlaylist, delete_playlist, tally_playlist 
from PlaylistDriver import sp, playlist_list
from PlaylistOperations import PlaylistOperations

load_dotenv()

app = Flask(__name__)

# Spotify connection — import this from PlaylistDriver instead of rewriting it

@app.route('/playlists')
def playlists():
    data = get_playlists()  # your function, unchanged
    return jsonify({"playlists": data})

@app.route('/top-tracks')
def top_tracks():
    results = sp.current_user_top_tracks(limit=10)
    tracks = []
    for track in results["items"]:
        tracks.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"]
        })
    return jsonify({"tracks": tracks})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
















