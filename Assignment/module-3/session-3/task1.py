# Write a Python function get_song_duration that takes a song name and returns its duration
# from a predefined dictionary. Use a try-except block to handle the case where the song is not 
# found and print 'Song not found on Spotify!'.

def get_song_duration(song_name):
    songs={"song A":"2:15","song B":"3:02","song C":"2:00"}

    try:
        #return songs[song_name]
        print("Duration:",songs[song_name])
    except Exception as e:
        print("Song not found on Spotify!")
        #return "Song not found on Spotify!"

song_name=input("enter song name:")
print(get_song_duration("song"))