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

from .Notes import Note
from .Scales import Scale
from .Signatures import Signature
from .Literals import parseKey
from itertools import chain

class Key:
  
  #key is a note
  def __init__(self, key = '', **options):
  
    default = {'simplify':True}
    options = {**default, **options}
    self.type = ''
    
    if not key:
      key = 'C'
    if isinstance(key, str):
      keyParts = parseKey(key)
      self.name = key
      self.literal = key
      self.root = Note(keyParts['tonic']) 
      self.sign = keyParts['alt']
      self.type = keyParts['type']
    elif isinstance(key, Note):
      self.name = key.name
      self.literal = key.name
      self.root = key 
      self.sign = key.sign
      
      
    self.notes = []   
    self.notesNames = []   
    
        
    if self.type == 'm':
      self.relative = Note(self.root.name).transpose(+3)
    else:
      self.relative = Note(self.root.name).transpose(-3)
      
    if options['simplify']:
      self.simplifyKey()  
      
    self.signature = Signature(self.root,self.type)
    self.sign = self.signature.sign
    
    self.notes = self.getNotes()
    self.notesNames = self.getNotesNames()
    
  def simplifyKey(self):
    #lors des transpositions, certains choix sont posés pour éviter des armures trop complexes
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
      
    
  def getScales(self):
    scales = []
    if self.type == 'm':
      scales.append(Scale(self.root,'mh')) #Mienur harmonique
      scales.append(Scale(self.root,'mm')) #Mienur mélodique
    else:
      scales.append(Scale(self.root,'major')) #Majeur
    return scales
    
  def getNotes(self):
    return Scale(self.literal).notes()
      
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
