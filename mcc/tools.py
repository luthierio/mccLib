
from mcc.note import Note
from mcc.chord import Chord
from mcc.key import Key

def isDiatonic(Chord, Key):
  test = True
  for note in Chord.notes:
    if note.name not in Key.notesNames:
      test = False
  return test


def getNonDiatonicNotes(Chord, Key):
  nonDiatonic = []
  for note in Chord.notes:
    if note.name not in Key.notesNames:
      nonDiatonic.append(note.name)
  return nonDiatonic      
