import os
import subprocess

# Define the playlist URL
playlist_url = input("Enter the URL of the YouTube playlist: ")


# Define the number of videos to download at once
video_batch = 10

# Check if the video has already been downloaded
def check_if_downloaded(video_title):
    return os.path.exists(f"{video_title}.mp3")

# Download the videos
for i in range(0, video_batch):
    try:
        # Use youtube-dl to download the video
        video = subprocess.run(
            [
                "youtube-dl",
                "-x",
                "--audio-format",
                "mp3",
                f"{playlist_url}?index={i}",
            ],
            capture_output=True,
            text=True,
        )

        # Get the video title
        video_title = video.stdout.split("\n")[0]

        # If the video has already been downloaded, skip it
        if check_if_downloaded(video_title):
            print(f"{video_title} has already been downloaded.")
            continue
    except Exception as e:
        # If there is an error, skip the video and print the error message
        print(f"Error downloading {video_title}: {e}")
        continue
