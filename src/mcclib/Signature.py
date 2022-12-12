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

from .Note import Note
from .literals import parseKey

class Signature:

  #Note is a note, type is 'm' or '' (=M) or 'M'
  def __init__(self, note, type = ''):
    
    self.type = type
    self.sign = ''
    
    if isinstance(note, str): 
      self.note = Note(note)
    elif isinstance(note, Note):   
      self.note = note
    else:
      raise ValueError(note," n'est pas une note duquel on peut déduire une signature")          
    
    if self.note.sign == "b":
      self.sign = "b"
    elif self.note.sign == "#":
      self.sign = "#"
    elif self.type == 'm':
      if self.note.name in ["F","C","G","D"]: 
        self.sign = 'b'
      elif self.note.name in ["E","B"]: 
        self.sign = '#'
    else: 
      if self.note.name in ["F"]: 
        self.sign = 'b'
      elif self.note.name in ["G","D","A","E","B"]: 
        self.sign = '#'
