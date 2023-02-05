#!/bin/bash

playlist_url="https://youtube.com/playlist?list=PLOAFzRws139CoGX2UvsGx5yWplrxBB6Hh"

while IFS= read -r url; do
    video_title="$(youtube-dl --get-title "$url")"
    video_filename="$video_title.mp3"
    if [ -f "$video_filename" ]; then
        echo "Skipping already downloaded file: $video_filename"
        continue
    fi

    echo "Downloading $video_title"
    youtube-dl --extract-audio --audio-format mp3 -o "$video_filename" "$url"
    if [ $? -ne 0 ]; then
        echo "Error downloading $video_title"
    fi
done < <(youtube-dl --flat-playlist --no-warnings "$playlist_url" | tail -n +2)

