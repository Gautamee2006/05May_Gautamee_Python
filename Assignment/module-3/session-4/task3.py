'''Add 2 more song names to my_fav_songs.txt without deleting the existing content,
 using Python's open() function in append ('a') mode.'''

f=open("my_fav_songs.txt","a")

#f.write("\nKesariya\nHeeriye")
song1=input("enter song name:")
song2=input("enter 2nd song name:")
f.write(f"\n{song1}\n{song2}")

print("song add successfuly")

f.close()