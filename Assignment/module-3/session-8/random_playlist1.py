'''Refactor your random_playlist.py so that the list of songs is defined in a separate module
 called songs.py. Import the list into your main script and use it for shuffling.
 <br><br><em><strong>Hint:</strong> Define your songs as a variable called song_list in songs.py 
 and import it using 'from songs import song_list'.</em>
'''
import random
from songs import song_list

random.shuffle(song_list)

print("Shuffled Playlist:")

for song in song_list:
    print(song)