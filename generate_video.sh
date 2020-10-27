#!/bin/sh

#ffmpeg -framerate 30 -i tracked_frames/%03d.png data/tracked.mp4
rm "data/tracked$1.mp4"
ffmpeg -framerate 30 -i tracked_frames/%03d.png -i "data/ants-song$1.mp3" "data/tracked$1.mp4"
