import re
from .note import Note


# distance of each notes from root
chordTypes = {
  "":[0,4,7], #Nothing specified means Major triad
  "7":[0,4,10],
  "M":[0,4,7],
  "M7":[0,4,7,11],
  "69":[0,4,7,9,14],
  "m":[0,3,7],
  "m6":[0,3,7,9],
  "m7":[0,3,7,10],
  "°":[0,3,6,9],
  "dim":[0,3,6,9],
  "m7b5":[0,3,7,9]
}  

class Chord:

  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, chord):
    self.name = ''
    self.root = ''
    self.alt = ''
    self.type = ''
    self.bass = ''
    self.intervals = []
    self.notes = []
    self.notesNames = []
    
    if isinstance(chord, str):
      self.parseLiteralChord(chord)
      #self.intervals = self.getInterval(self.num)
    
  def parseLiteralChord(self,lc):
    
    self.name = lc
    chordParts = re.search('(([ABCDEFG])([b|#])?)([A-Za-z0-9°]*)?([/][A-Z][b|#]?)?', lc)
    self.root = Note(chordParts.group(1))
    self.sign = chordParts.group(3) if chordParts.group(3) else ''
    self.type = chordParts.group(4) if chordParts.group(4) else ''
    if chordParts.group(5):
    	self.bass = Note(chordParts.group(5)[1:],self.sign)
    
    self.intervals = chordTypes[self.type]
    self.update()
          
  
  def getNotesNames(self):
    self.notesNames = []
    for note in self.notes:
      self.notesNames.append(note.name)
    return self
    
  def transpose(self, interval):
    self.root.transpose(interval)
    self.update()
    return self
            
  def update(self):
    self.notes = []
    self.notesNames = []
    if isinstance(self.bass,Note):
      self.notes.append(self.bass)
      self.notesNames.append(self.bass.name)
    for interval in self.intervals:
      note = Note(self.root.index+interval,self.sign)
      self.notes.append(note)
      self.notesNames.append(note.name)
    return self
  
  def print(self):
    print(self,'\t',self.type,'\t',self.bass,'\t',self.intervals,'\t',self.notesNames)
    
  def __str__(self):
    return f"{self.root.name}{self.type}"
  
