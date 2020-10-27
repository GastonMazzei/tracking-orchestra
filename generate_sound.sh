#!/bin/sh
rm "data/ants-song$1.mp3"
python3 "scripts/midi_maker$1.py"
timidity "data/ants-song$1.mid" -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k "data/ants-song$1.mp3"
