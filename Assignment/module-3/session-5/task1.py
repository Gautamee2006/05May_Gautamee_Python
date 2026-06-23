# Create a Python class called Song with attributes title, artist, 
# and duration (in seconds). Use the __init__ method to initialize
# these attributes and create two Song objects with different values.

class song:
    def __init__(self,title,artist,duration):
        self.title=title
        self.artist=artist
        self.duration=duration

title1=input("enter song name:")
artist1=input("enter artist of this song:")
duration1=input("enter duration of this song(in seconds):")

title2=input("enter song name:")
artist2=input("enter artist of this song:")
duration2=input("enter duration of this song(in seconds:)")

song1=song(title1,artist1,duration1)
song2=song(title2,artist2,duration2)

print()
print("-------details of song 1:-------")
print("song name:",song1.artist)
print("song artist:",song1.artist)
print("song duration:",song1.duration,"secound")

print()
print("-------details of song 2:-------")
print("song name:",song2.artist)
print("song artist:",song2.artist)
print("song duration:",song2.duration,"secound")