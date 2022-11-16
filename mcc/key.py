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
import re
from .note import Note
#! numéros de notes, donc intervales depuis la fondamentale des notes de la gamme
majorScale = [0,2,4,5,7,9,11]
minorScale = [0,2,3,5,7,8,10]

class Key:
  
  #key is a note
  def __init__(self, key = 'C'):
  
    keyParts = re.search('(([ABCDEFG])([b|#])?)([mM])?', key)
    self.src = key
    self.notes = []    
    
    self.root = Note(keyParts.group(1))
    self.alt =  keyParts.group(3) if keyParts.group(3) else ''  
    self.type = keyParts.group(4) if keyParts.group(4) else ''  
    
    if self.type == 'm':
      self.relative = Note(self.root.name).transpose(+3)
    else:
      self.relative = Note(self.root.name).transpose(-3)
    self.simplifyKey()   
    self.setNotes()
    self.setName()
    
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

  def setNotes(self):
    self.notes = []
    if self.type =='m': 
      scale = minorScale
    else:
      scale = majorScale
      
    for noteNum in scale:
      self.notes.append(Note(self.root.num+noteNum, self.root.keyType).name)    
    return self
      
  def setName(self):  
    self.name = self.root.name+self.root.keyType
    return self
        
  def transpose(self,interval):
    self.root.transpose(interval)
    self.__init__(self.root.name)
    return self
    
  def isSimplified(self):
    return True if self.src != self.name else False
    
  def print(self):
    print(self,'\t',self.alt,'\t',self.isSimplified(),'\t',self.src,self.notes)
    
  def __str__(self):
    return f"{self.root}{self.type}"
