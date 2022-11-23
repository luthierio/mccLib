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
#! numéros de notes, donc intervales depuis la fondamentale des notes de la gamme
majorScale = [0,2,4,5,7,9,11]
minorScale = [0,2,3,5,7,8,10,11]

class Key:
  
  #key is a note
  def __init__(self, key = 'C', **options):
  
    default = {'simplify':True}
    options = {**default, **options}
    
    keyParts = re.search('(([ABCDEFG])([b|#])?)([mM])?', key)
    self.name = key
    self.src = key
    self.notes = []   
    self.notesNames = []   
    
    self.root = Note(keyParts.group(1)) 
    self.sign = ''  
    self.type = keyParts.group(4) if keyParts.group(4) else '' 
    if self.type == 'm':
      self.relative = Note(self.root.name).transpose(+3)
    else:
      self.relative = Note(self.root.name).transpose(-3)
      
    if options['simplify']:
      self.simplifyKey()  
    self.setSignature()
    
    self.notes = self.getNotes()
    self.notesNames = self.getNotesNames()
    
  def simplifyKey(self):
    equiv = {
      'Fb':'E', #oublier Fab
      'E#':'F', #oublier Mi#
      'B#':'C', #oublier Si#
      'Cb':'B', #oublier Dob
    }
    for fromkey, tokey in equiv.items():
      if self.root.name == fromkey:
        self.root = Note(tokey)
        self.__init__(self.root.name+self.type)
    
    if self.type =='m': 
      substitutions = {
        'Gb':'F#', 
        'Db':'C#', 
        'G#':'Ab', 
        'A#':'Bb',
      }
    else:
      substitutions = {
        'G#':'Ab', #éviter Sol #
        'D#':'Eb', #éviter Ré #  (9#)
        'A#':'Bb', #éviter La #
        'F#':'Gb', #choix courant ... 6 bémols vs 6#
        'C#':'Db', #éviter Do #  (7#)
      }
    for fromkey, tokey in substitutions.items():
      if self.root.name == fromkey:
        self.root = Note(tokey)
        self.__init__(self.root.name+self.type)
    return self
    
  def setSignature(self):
    if self.type == 'm' and self.root.name in ["Ab","Eb","Bb","F","C","G","D"]: 
      self.sign = 'b'
    elif self.type == 'm' and self.root.name in ["E","B","F#","C#","G#","D#","A#"]: 
      self.sign = '#'
    elif self.type != 'm' and self.root.name in ["Cb","Gb","Db","Ab","Eb","Bb","F"]: 
      self.sign = 'b'
    elif self.type != 'm' and self.root.name in ["G","D","A","E","B","F#","C#"]: 
      self.sign = '#'
  
  def getNotes(self):
    notes = []
    if self.type =='m': 
      scale = minorScale
    else:
      scale = majorScale
      
    for noteNum in scale:
      note = Note(self.root.index+noteNum, self.sign)
      notes.append(note)     
    return notes
      
  def getNotesNames(self):
    names = []
    for note in self.notes:
      names.append(note.name)
    return names 
      
  def getNotesIndex(self):
    indexes = []
    for note in self.notes:
      indexes.append(note.index)
    return indexes  
  
  def setName(self):  
    self.name = self.root.name+self.type
    return self
        
  def transpose(self,interval):
    self.root.transpose(interval)
    self.__init__(self.root.name+self.type)
    return self
    
    
  def print(self):
    print(self,'\t',self.root.name,'\t',self.type,'\t',self.name,'\t',self.sign,'\t',self.notesNames)
    
  def __str__(self):
    return f"{self.root}{self.type}"
