import requests
import base64
import json

# Register your app to get client_id and client_secret - https://developer.spotify.com/dashboard/applications
client_id = "TODO"
client_secret = "TODO"

# Follow these instruction to get the following - https://github.com/spotify/web-api-auth-examples
redirect_uri = "http://localhost:8888/callback"
access_token = "TODO"
refresh_token = "TODO"

def use_refresh_token_for_new_access_token():

    # Get new access token
    url = "https://accounts.spotify.com/api/token"
    b64encoded_data = base64.b64encode((client_id + ":" + client_secret).encode("utf-8")).decode("utf-8")
    headers = {"Authorization": "Basic " + b64encoded_data}
    r = requests.post(url, headers=headers, data={"grant_type": "refresh_token", "refresh_token": refresh_token})
    token_data = r.json()

    # Return the access token
    return token_data["access_token"]

def add_song_to_playlist(song_uri, playlist_id):
    add_song_url = "https://api.spotify.com/v1/playlists/" + str(playlist_id) + "/tracks?uris=" + str(song_uri);
    access_token = use_refresh_token_for_new_access_token()
    headers = {"Authorization": "Bearer " + access_token}
    r = requests.post(add_song_url, headers=headers)

def get_current_song():
    current_track_url = "https://api.spotify.com/v1/me/player/currently-playing"
    access_token = use_refresh_token_for_new_access_token()
    headers = {"Authorization": "Bearer " + access_token}
    r = requests.get(current_track_url, headers=headers)
    cur_track_info = json.loads(r.text)
    return cur_track_info["item"]["uri"]

def get_jams_playlist():
    total = 1000000
    limit = 50;
    offset = 0;

    # Paginate playlists
    while(offset-limit < total):
        current_track_url = "https://api.spotify.com/v1/me/playlists?limit=" + str(limit) + "&offset=" + str(offset)
        access_token = use_refresh_token_for_new_access_token()
        headers = {"Authorization": "Bearer " + access_token}
        r = requests.get(current_track_url, headers=headers)
        playlists = json.loads(r.text)
        # This should be the name of the playlist you want to add to
        playlist_title = "Adam and Cayce's Jams"

        for playlist in playlists["items"]:
            if playlist["name"] == playlist_title:
                return playlist["uri"]

        offset += limit
        total = playlists['total']

    print("playlist not found")


if __name__ == "__main__":

        # Get the currently playing song
        song_uri = get_current_song()
        # Find the playlist you want to add to
        playlist_id = get_jams_playlist()[17:]
        # Add song to playlist
        add_song_to_playlist(song_uri, playlist_id)
