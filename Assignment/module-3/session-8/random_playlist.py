'''Create a random_playlist.py script that uses the random module to shuffle a list of 5 of your
favorite songs (just song names as strings) and prints the shuffled playlist each time you run it.'''


import random

songs = [
    "Kesariya",
    "Tum Hi Ho",
    "Perfect",
    "Believer",
    "Shape of You"
]

random.shuffle(songs)

print("Shuffled Playlist:")
for song in songs:
    print(song)