#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#    Simon Daron 2022

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
  "m7b5":[0,3,7,9],
  "ø":[0,3,7,9],
  "+":[0,4,8,10],
  "5+":[0,4,8,10],
}  

class Chord:

  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, chord):
    self.chord = chord
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
    chordParts = re.search('(([ABCDEFG])([b|#])?)([A-Za-z0-9°ø+]*)?([/][A-Z][b|#]?)?', lc)
    if not chordParts:
      raise Exception("Format d'accord incorrect", lc,self.chord)
      
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
    
  def transpose(self, interval, sign = ''):
  
    self.root.transpose(interval, sign)
    if self.bass:
      self.bass.transpose(interval, sign)
    self.__init__(self.__str__())
    
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
  
    if self.bass:
      return self.root.name+self.type+'/'+self.bass.name
    else:
      return self.root.name+self.type
  
