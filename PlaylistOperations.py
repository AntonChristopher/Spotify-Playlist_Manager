#Playlist Operations Class
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
load_dotenv()


class PlaylistOperations:
    def __init__(self, sp, playlist_id):
        self.sp = sp
        self.playlist_id = playlist_id
        self.playlist_name = self.sp.playlist(self.playlist_id)["name"]
    
    def add_tracks_to_playlist(self, new_tracks_list):
        self.sp.playlist_add_items(self.playlist_id, new_tracks_list)

    def delete_playlist(self):
        self.sp.current_user_unfollow_playlist(self.playlist_id)

    def get_top_tracks(self, limit=10):
        results = self.sp.current_user_top_tracks(limit=limit)
        track_id_list = [track["id"] for track in results["items"]]
        return track_id_list
    
    def union_playlist_tracks(self, new_tracks_list):
        track_result = list(set(self._get_track_list()) | set(new_tracks_list))
        self.add_tracks_to_playlist(new_tracks_list)
    
    def display_tracks(self):
        count = 0
        for item in self.sp.playlist_tracks(self.playlist_id)["items"]:
            count += 1
            print(str(count) + ". " + item["item"]["name"])

    def _get_track_list(self):
        return [item["track"]["id"] for item in self.sp.playlist_tracks(self.playlist_id)["items"]]
    
    def format_dict(self):
        return {"name": self.playlist_name, "id": self.playlist_id}
            



