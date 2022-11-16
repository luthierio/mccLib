import re
from .note import Note

class Chord:

  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, chord):
    self.name = ''
    self.root = ''
    self.alt = ''
    self.type = ''
    self.intervals = []
    self.notes = []
    
    if isinstance(chord, str):
      self.parseLiteralChord(chord)
      #self.intervals = self.getInterval(self.num)
    
  def parseLiteralChord(self,lc):
    
    self.name = lc
    chordParts = re.search('(([ABCDEFG])([b|#])?)(.*)', lc)
    self.root = Note(chordParts.group(1))
    self.alt = chordParts.group(3) if chordParts.group(3) else ''
    self.type = chordParts.group(4) if chordParts.group(4) else ''
    
    self.intervals = chordTypes[self.type]
    for interval in self.intervals:
      self.notes.append(Note(self.root.num+interval,self.alt))
          
  
  def getNotesNames(self):
    notNames = []
    for note in self.notes:
      notNames.append(note.name)
    return notNames
    
  def transpose(self, interval):
    self.root.transpose(interval)
    self.notes = []
    for interval in self.intervals:
      self.notes.append(Note(self.root.num+interval,self.alt))
        
  def __str__(self):
    return f"{self.root.name}{self.type}"
  

# distance of each notes from root
chordTypes = {
  "":[0,4,7], #Nothing specified means Major triad
  "M":[0,4,7],
  "m":[0,3,7],
  "m6":[0,3,7,9]
}  
