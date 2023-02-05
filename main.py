import os
import subprocess

# YouTube playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLOAFzRws139CoGX2UvsGx5yWplrxBB6Hh"

# Output directory for the downloaded files
output_dir = "/"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# The number of videos to download per request
download_count = 10

# Counter for the total number of videos downloaded
total_downloaded = 0

# Loop through all the videos in the playlist
while True:
    # YouTube-dl command to download the videos as audio files
    command = f"youtube-dl -o '{output_dir}/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --playlist-end {download_count} {playlist_url}"

    # Execute the command and capture the output
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # If the command completed successfully, break out of the loop
    if result.returncode == 0:
        break

    # If the command failed, print the error messages and skip the failed videos
    error_messages = result.stderr.decode("utf-8").strip().split("\n")
    failed_videos = []
    for error_message in error_messages:
        if "ERROR:" in error_message:
            video_title = error_message.split(" ")[-1]
            failed_videos.append(video_title)
    print(f"The following videos could not be downloaded: {failed_videos}")

    # Update the playlist URL to skip the failed videos
    playlist_url = f"{playlist_url}&index={total_downloaded + download_count}"
    total_downloaded += download_count
