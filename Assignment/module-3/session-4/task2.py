'''Write a function add_song_to_playlist(song_name, playlist) for a Spotify-like app that raises a
 SongAlreadyExistsError (custom exception) if the song is already present in the playlist.
 <br><br><em><strong>Hint:</strong> Define SongAlreadyExistsError as a user-defined exception 
 class and use the raise keyword inside your function.</em>'''

class SongAlreadyExistsError(Exception):
    pass

def add_song_to_playlist(song_name, playlist):
    
    try:

        if song_name in playlist:
            raise SongAlreadyExistsError("song already exists in tha playlist..")
        
        else:
            print("song add succesfully!")
            playlist.append(song_name)
            print("update playlist:",playlist)

    except SongAlreadyExistsError as e:
        print("ERROR:",e)

playlist=["Kesariya","Heeriye","Apna Bana Le","Raataan Lambiyan"]

song_name=input("enter song name:")

add_song_to_playlist(song_name,playlist)