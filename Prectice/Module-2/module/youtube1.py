from pytubefix import YouTube

url = input("YouTube URL: ")

yt = YouTube(url)

print("Title:", yt.title)

#video = yt.streams.get_highest_resolution()
video = yt.streams.get_audio_only()

video.download(output_path="E:/python/YouTube_Videos")

print("Download Complete!")