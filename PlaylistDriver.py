import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
from PlaylistOperations import PlaylistOperations
import json
load_dotenv()


#FUNCTIONS
#creates playlist and returns True if it doesn't already exist, otherwise returns False
def createPlaylist(sp, playlist_name):
    #load json dictionary to data
    name_to_compare = playlist_name.lower().strip()
    data = get_playlists()

    for item in data:
         if item["name"].lower().strip() == name_to_compare:
            playlist_list.append(PlaylistOperations(sp, item["id"]))
            return False
    #otherwise, create a new playlist of that name and return id
    playlist = sp.current_user_playlist_create(playlist_name, False, False, "This playlist is an API-created playlist via a Python script I wrote! ")
    po = PlaylistOperations(sp, playlist["id"])
    playlist_list.append(po)
    tally_playlist(po.format_dict())
    return True

#one more comment guys
def listPlaylists():
    print("\nHere are your playlists:")
    if len(playlist_list) > 0:
        count1 = 0
        for item in playlist_list:
            print(count1, ". ", item.playlist_name)
            count1 += 1
    else:
        print("You don't have any playlists!")

#Returns a list of dictionaries of names and ids
def get_playlists():
    try:
        with open("playlists.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        data = []
    return data

#Adds the playlist to the json file
def tally_playlist(single_playlist_dict):
    data = get_playlists()
    data.append(single_playlist_dict)
    with open("playlists.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

#Deletes playlist for account, from playlists.json, and from playlists_list
def delete_playlist(po):
    po.delete_playlist() #for account
    data = get_playlists()
    data.remove(po.format_dict()) #from json
    with open("playlists.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    playlist_list.remove(po) #from playlist_list




    #VARIABLES 
    #Client variables
playlist_list = []
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
scope = "user-top-read playlist-modify-private playlist-modify-public playlist-read-private"

#object of the Spotify class
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".cache"   # explicit path
        ))

# LOAD starting playlists
for item in get_playlists():
    playlist_list.append(
        PlaylistOperations(sp, item["id"])
    )

if __name__ == '__main__':
    options_list = [
        "0. Quit the program",
        "1. List your playlists",
        "2. Create a playlist",
        "3. Delete a playlist",  #should only be able to delete playlists created by the program
        "4. List the tracks in a playlist",
        "5. Add tracks to a playlist",
        "6. Remove tracks from a playlist"
    ]


    user_choice = ""
    #User choice of action
    while (user_choice != "0"):
        print("\n")
        for s in options_list:
            print(s)
        user_choice = input("Enter the number of your choice: ")
        print("\n")

    #operations on the list of playlists
        #list playlists
        if user_choice == "1":
            listPlaylists()

        #create a playlist
        elif user_choice == "2":
            input_name = input("Enter the name of your new playlist: ")
            did_create = createPlaylist(sp, input_name)
            if did_create:
                print("playlist ", input_name, " has been created!")
            else:
                print(input_name, "is already a playlist! Try a new name")

        #Delete a playlist
        elif user_choice == "3":
            listPlaylists()
            input_num = int(input("Enter the number of the playlist to delete: "))
            if input_num < len(playlist_list):
                delete_playlist(playlist_list[input_num])
            else:
                print("Index out of range, sorry")

    #Operations on a chosen playlist        
        else:
            listPlaylists()
            if len(playlist_list) > 1:
                input_num = int(input("Enter the number of your playlist choice: "))
            else:
                input_num = 0
            if input_num < len(playlist_list):
                playlist = playlist_list[input_num]
            else:
                print("Sorry, invalid choice")
                continue

            if user_choice == "4":
                playlist.display_tracks()

            elif user_choice == "5":
                query = input("Enter song name (or song + artist): ").strip()
                tracks = sp.search(q=query, type="track", limit=10)["tracks"]["items"]
                if not tracks:
                    print("No songs found.")
                else:
                    count2 = 0
                    for t in tracks:
                        print(count2, ". ", tracks[count2]["name"])
                        count2 += 1
                    choice = int(input("Choose a song number: "))
                    track_id = tracks[choice]["id"]
                    playlist.add_tracks_to_playlist([track_id])
                    print(tracks[choice]["name"], " was added.")
            
            
                
            


    print("\nThank you! Have a nice day!")


















