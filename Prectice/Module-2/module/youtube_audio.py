from pytubefix import YouTube

url = input("YouTube URL: ")

yt = YouTube(url)

print("Title:", yt.title)

audio = yt.streams.filter(only_audio=True).first()

audio.download(output_path="E:/python/YouTube_Audio")

print("Audio Download Ho Gaya!")