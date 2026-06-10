# Build a script that reads all lines from my_fav_songs.txt, counts how many songs are listed, and displays 'Total songs: X' at the end.<br><br><em><strong>Hint:</strong> Use the readlines() method to get all lines as a list and len() to count.</em>

f=open("my_fav_songs.txt","r")

song=f.readlines()
print(song)

lenofsong=len(song)
print("total songs:",lenofsong)