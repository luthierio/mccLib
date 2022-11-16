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

_note_dict = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
noteNames = ["C","","D","","E","F","","G","","A","","B"]

class Note:
  
  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, note, context = ''):
    
    self.context =  context if context else '#'
    
    self.root = '' #Si altération, la racine de la note: C#, root = C
    self.alt = 0 # b = -1, # = +1
    self.name = ''
    self.temperName = ''
    self.num = ''

    if isinstance(note, str):
    
      if context == '' and len(note) > 1:    
        self.context = note[1]
        
      self.num = self.getNumFromName(note)
      self.name = self.getNameFromNum(self.num)
        
    elif isinstance(note, int):
      self.num = self.getIndexFromNum(note)
      self.name = self.getNameFromNum(self.num)
  
      
  def getIndexFromNum(self,num):
    if abs(num) not in range(0, 11):
      num = num % 12
    if num < 0:
      num = 12+num
    return num
              
  def getNameFromNum(self,num):
      
    if noteNames[num]:
      return noteNames[num]
    else:        
      if self.context == 'b':
        return noteNames[num+1]+'b'
      else:
        return noteNames[num-1]+'#'
        
  def getNumFromName(self,name): 
   
      if len(name) > 1:
        nbrAlt = len(name)-1
        root = name[0]
        if name[1] == '#':
          alt = nbrAlt
        elif name[1] == 'b':
          alt = -nbrAlt
      else:
        root = name  
        alt = 0    
      
      return self.getIndexFromNum(noteNames.index(root)+alt)
           
  def transpose(self,interval):  
   self.num = self.getIndexFromNum(self.num+interval)
   self.name = self.getNameFromNum(self.num)
   return self
    
  def __str__(self):
    return f"{self.name} ({self.num})"
