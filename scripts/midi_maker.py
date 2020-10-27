import numpy as np

from collections import namedtuple

from mido import Message, MetaMessage, MidiFile
from mido.midifiles import MidiTrack
import mido

def add_notes(track, notes, pos_in_secs,tpb,tempo):
    times_in_ticks = [mido.second2tick (x, tpb, tempo) for x in pos_in_secs]
    timedelta = mido.second2tick (1/30, tpb, tempo)
    print(timedelta)
    timedelta = int(timedelta)
    deltas = [0]+np.diff(times_in_ticks).tolist()
    for ix, note in enumerate(notes):
        time_delta_in_ticks = deltas[ix]

        track.append(
            Message(
                'note_on',
                note=note['note'],
                velocity=note['velocity'],
                time = 0
            )
        )
        if True:
          track.append(
            Message(
                'note_off',
                note=note['note'],
                velocity=note['velocity'],
                time = timedelta
            )
        ) 
    print(tpb)
    print('last index was ',ix)

def map_note(xpx):
  return  int(10 + 110*xpx/2000)

def map_volume(ypx):
  return int(10 + 110*ypx/700)

def create_midi_file_with_notes(filename, bpm=112.5): 
    array = np.load('data/tracks_positions.npy')
    #[max_0,max_1],[min_0,min_1] = [f(array[:,:2]) for f in [lambda x:np.max(x,0), lambda x:np.min(x,0)]]
    #print(max_0,max_1,min_0,min_1) 
    pos_in_secs = [j/30 for j in range(len(array[:,0]))]
    notes = [{'note': map_note(v[0]) ,
              'velocity':map_volume(v[1]),
              #'time':pos_in_secs[j],
              } for j,v in enumerate(array.tolist())]
    tpb=480 #ticks per beat
    with MidiFile(ticks_per_beat=tpb) as midifile:
        track = MidiTrack()
        midifile.tracks.append(track)
        track.append(Message('program_change', program=12, time=0))
        tempo = mido.bpm2tempo(bpm)
        sec_per_tick = 1/((tempo * midifile.ticks_per_beat) / 60 )
        add_notes(track, notes, pos_in_secs, tpb, tempo)
        midifile.save('{}.mid'.format(filename)) 
if __name__=='__main__':
  create_midi_file_with_notes('data/ants-song')
