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
    for ix, note in enumerate(notes):
        track.append(
            Message(
                'note_on',
                note=note['note'],
                velocity=note['velocity'],
                time = 0
            )
        )
        print(note['velocity'])
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



def create_midi_file_with_notes(filename, bpm=112.5): 
    array = np.load('data/tracks_positions_multiple.npy', allow_pickle=True)
    with open('data/number_of_boxes.txt','r') as f:
      for ij,l in enumerate(f.readlines()):
        if ij==0: L = int(l)
        elif ij==1: maximum_x= int(l)
        else: maximum_y = int(l)
    v = [[] for x in range(L)]
    print(v, L)
    for i,x in enumerate(array):
      try:
        if not bool(x): print('passed')
      except:
        for j in range(L):
          v[j].append(x[j].tolist())    
    pos_in_secs = [j/30 for j in range(len(v))]
    notes = []
    for a_,array in enumerate(v):
      BASE_NOTE, PEAK_NOTE, BASE_VOL, PEAK_VOL = 40+a_*0,70+a_*0,50,70
      def map_note(xpx,maximum_x):
        output = int(BASE_NOTE + PEAK_NOTE*(xpx//4)*4/maximum_x)
        return output
      def map_volume(ypx,maximum_y):
        return int((BASE_VOL + PEAK_VOL*ypx/maximum_y))
      notes.append([{'note': map_note(v[0],maximum_x) ,
              'velocity':map_volume(v[1],maximum_y),
              #'time':pos_in_secs[j],
              } for v in array])
    tpb=480 #ticks per beat
    with MidiFile(ticks_per_beat=tpb) as midifile:
        tracks = [MidiTrack() for i_ in range(L)]
        for j_ in range(L):
          track = tracks[j_]
          midifile.tracks.append(track)
          track.append(Message('program_change', program=59, time=0))
          tempo = mido.bpm2tempo(bpm)
          sec_per_tick = 1/((tempo * midifile.ticks_per_beat) / 60 )
          add_notes(track, notes[j_], pos_in_secs, tpb, tempo)
        midifile.save('{}.mid'.format(filename))
        for t in midifile.tracks:
          print(t)
          
if __name__=='__main__':
  create_midi_file_with_notes('data/ants-songs')
