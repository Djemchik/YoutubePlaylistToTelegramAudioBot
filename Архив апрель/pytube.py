import pytube
import os
from pytube import Playlist
# The playlist URL
url = "https://www.youtube.com/playlist?list=PLOAFzRws139CoGX2UvsGx5yWplrxBB6Hh"

# Get all the video URLs from the playlist
playlist = pytube.playlist(url)
video_urls = playlist.video_urls



from pytube import Playlist

playlist = url
print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

for video in playlist.videos:
    video.streams.first().download


# Download each video, up to 10 at a time
downloaded = 0
for video_url in video_urls:
    if downloaded >= 10:
        break
    try:
        video = pytube.YouTube(video_url)
        video_title = video.title
        if not os.path.exists(f"{video_title}.mp3"):
            video.streams.filter(only_audio=True).first().download(filename=video_title)
            downloaded += 1
        else:
            print(f"Skipping {video_title}.mp3 as it already exists.")
    except:
        print(f"Could not download {video_title}.mp3")
