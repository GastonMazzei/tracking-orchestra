#!/bin/sh

ffmpeg -i $1.mp4 -ss 00:00:$2 -t 00:00:$3 -async 1 $1-out.mp4
rm $1.mp4
ffmpeg -i $1-out.mp4 -filter:v fps=fps=30 $1.mp4
rm $1-out.mp4
