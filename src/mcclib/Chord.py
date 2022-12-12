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
from .Note import Note
from .Key import Key


# distance of each notes from root
# https://theoriemusicale.camilleroux.com/accords/
chordTypes = {
  ""    :[0,4,7], #Nothing specified means Major triad
  "M"   :[0,4,7],
  "M7"  :[0,4,7,11],
  "Δ"   :[0,4,7,11],
  "M6"  :[0,4,7,9],
  "69"  :[0,4,7,9,14],
  "6"   :[0,4,7,9   ],
  "9"   :[0,4,7,  14],
  "9+"  :[0,4,7,  15],
  
  "13"  :[0,4,7,  8],
  "13b9":[0,4,7,  8,13],
  
  "m"   :[0,3,7],
  "m6"  :[0,3,7,9],
  "mb6" :[0,3,7,8],
  "m7"  :[0,3,7,10],
  "mΔ"  :[0,3,7,11],
  "m9"  :[0,3,7,14],
  "m11" :[0,3,7,5],# A vérifier
  
  "7"   :[0,4,7,10],
  "9"   :[0,4,7,10,14],
  "9b"   :[0,4,7,10,13],
  "9b5" :[0,4,6,10,14],
  "79"  :[0,4,7,10,14],
  "7b9" :[0,4,7,10,13],
  "7b13":[0,4,7,10,8],  #b13 = #5
  
  "7+"  :[0,4,8,10],# A vérifier
  "+7"  :[0,4,8,10],# A vérifier
  "7aug":[0,4,8,10],# A vérifier
  "7#5" :[0,4,8,10],# A vérifier
  "75+" :[0,4,8,10],# A vérifier
  
  "7b5" :[0,4,6,10],# A vérifier
  
  "7sus" :[0,5,7,10],# A vérifier
  "7sus4":[0,5,7,10],# A vérifier
  
  "°"   :[0,3,6,9],
  "0"   :[0,3,6,9],
  "dim" :[0,3,6,9],
  
  "m7b5":[0,3,7,9],
  "ø"   :[0,3,7,9],
  
  "+"   :[0,4,8],
  "+Δ"  :[0,4,8,11],
  "5+"  :[0,4,8],
  "aug" :[0,4,8],
  
  "5+11+"  :[0,4,8,6],
  #"3b9"  :[0,1,2,3,4,5,6,7,8,9,10,11],
}  

class Chord:

  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, chord, key= Key()):
    self.literal = chord
    self.key = key
    self.name = ''
    self.root = ''
    self.alt = ''
    self.type = ''
    self.bass = ''
    self.intervals = []
    self.notes = []
    self.notesNames = []
    
    if isinstance(self.literal, str):
      self.parseLiteralChord(self.literal)
      #self.intervals = self.getInterval(self.num)
      self.notes = self.getNotes()
      self.notesNames = self.getNotesNames()
      
  def parseLiteralChord(self,lc):
      
    self.name = lc
    chordParts = re.search('(([ABCDEFG])([b|#])?)([A-Za-z0-90-9°ø+]*)?([/][A-Z][b|#]?)?', lc)
    if not chordParts:
      print("Format d'accord incorrect",lc,self.literal)
      #return False
      raise Exception("Format d'accord incorrect: '"+self.literal+"'")
      
    self.sign = chordParts.group(3) if chordParts.group(3) else self.key.sign
    self.root = Note(chordParts.group(1),self.sign)
    self.type = chordParts.group(4) if chordParts.group(4) else ''
    if chordParts.group(5):
    	self.bass = Note(chordParts.group(5)[1:],self.sign)
    
    self.intervals = chordTypes[self.type]
      
  def transpose(self, interval, sign = ''):
  
    self.root.transpose(interval, sign)
    if self.bass:
      self.bass.transpose(interval, sign)
    self.__init__(self.__str__())
    
    return self
  
  def getNotes(self):
    notes = []
    if isinstance(self.bass,Note):
      notes.append(self.bass)
    for interval in self.intervals:
      note = Note(self.root.index+interval,self.sign)
      notes.append(note)
    return notes
    
  def getNotesNames(self):
    names = []
    for note in self.notes:
      names.append(note.name)
    return names 
    
  def isDiatonic(self, key = False):
    if not key:
      key = self.key
    test = True
    for note in self.notes:
      if note.index not in key.getNotesIndex():
        return False
    return test
    
  def getNonDiatonicNotes(self, key = False):
    if not key:
      key = self.key
    nonDiatonic = []
    for note in self.notes:
      if note.index not in key.getNotesIndex():
        nonDiatonic.append(note)
    return nonDiatonic      
  
  def print(self):
    print(self,'\t',self.type,'\t',self.bass,'\t',self.intervals,'\t',self.notesNames)
    
  def __str__(self):
  
    if self.bass:
      return self.root.name+self.type+'/'+self.bass.name
    else:
      return self.root.name+self.type
  
