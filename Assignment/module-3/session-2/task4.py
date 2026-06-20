# Given a file called playlist.txt containing song names (one per line),
# write code to jump to the start of the third song using seek() and readline(), 
# then print only that song's name.<br><br><em><strong>Constraint:</strong> 
# Do not read the whole file into memory at once.</em>

f=open("playlist.txt","r")

print("current position:",f.tell())

f.readline()
f.readline()

p=f.tell()

f.seek(p)

song=f.readline()

print(song.strip())

f.close()