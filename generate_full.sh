#!/bin/sh

echo "Initializing the project! (creating a directory for the frames)"
echo "\nSpecial Note: calling this script with the flag 's' allows multi-tracking!\n"
echo "$1"
bash clean.sh >> logs.txt
mkdir tracked_frames >> logs.txt
echo "generating frames!"
bash generate_frames.sh $1 $2>> logs.txt
echo "generating sound!"
bash generate_sound.sh $1 >> logs.txt
echo "generating video!"
bash generate_video.sh $1 >> logs.txt
echo "cleaning up (erasing the directory and logs)"
#bash clean.sh >> logs.txt 
#rm -r tracked_frames >> logs.txt
#rm logs.txt
echo "Opening the result!"
xdg-open "data/tracked$1.mp4"
echo "ENDED!"
