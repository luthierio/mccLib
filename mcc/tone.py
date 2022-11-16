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

from .note import Note

class Tone:
  
  #Tone is a note
  def __init__(self, tone = 'C'):
    self.keyType = ''
    self.fondamentale = Note(self.manageComplexTones(tone))
    self.update()
    
  def manageComplexTones(self,tone):
    replacements = {
      'C#':'Db',
      'D#':'Eb',
      'F#':'Gb',
      'G#':'Ab',
      'A#':'Bb',
      'Cb':'Bb',
    }
    for fromTone, toTone in replacements.items():
      if tone == fromTone:
        return toTone
      return tone
  
  def update(self):
    self.keyType = self.getKeyType()
  
  def getKeyType(self):
    if self.fondamentale.name in ["G","D","A","E","B"]:
      return '#'
    elif self.fondamentale.name in ["F","Bb","Eb","Ab","Db","Gb"]:
      return 'b'      
    return ''
    
  def print(self):
    print(self,'\t',self.keyType)
    
  def __str__(self):
    return f"{self.fondamentale}"
