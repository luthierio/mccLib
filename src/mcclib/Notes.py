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

noteNames = ["C","","D","","E","F","","G","","A","","B"]

class Note:
  
  #Note is a integer from 0 to 11 or a name C#... sign force use of 'b' or '#' to name unamed notes
  def __init__(self, note, context = None):
    
    from .Scales import Scale
    from .Chords import Chord
    
    self.context = context
    if isinstance(context, str):
      self.sign =  context
    elif isinstance(context, Scale):
      self.sign = context.signature.sign
    elif isinstance(context, Chord):
      self.sign = context.sign
    
    self.root = '?' #Si altération, la racine de la note: C#, root = C
    self.alt = ''
    self.name = ''
    self.index = '' 

    if isinstance(note, str):
      self.name = note
      self.index = self.getIndexFromName(note)
        
    elif isinstance(note, int):
      self.index = self.getIndexFromNum(note)    
      self.name = self.getNameFromIndex(self.index)

    if len(self.name) == 2:    
      self.root = self.name[0]
      self.alt = self.name[1]       
    elif len(self.name) == 1:
      self.root = self.name
    
    if not hasattr(self,'sign'):
      self.sign = self.alt
    
            
  def getIndexFromNum(self,num):
    if abs(num) not in range(0, 11):
      num = num % 12
    if num < 0:
      num = 12+num
    return num
              
  def getNameFromIndex(self,num):
      
    if noteNames[num]:
      return noteNames[num]
    else:        
      if self.sign == 'b':
        return noteNames[num+1]+'b'
      else:
        return noteNames[num-1]+'#'
        
  def getIndexFromName(self,name): 
      alt = 0    
      if len(name) > 1:
        nbrAlt = len(name)-1
        root = name[0]
        if name[1] == '#':
          alt = nbrAlt
        elif name[1] == 'b':
          alt = -nbrAlt
      else:
        root = name  
      
      return self.getIndexFromNum(noteNames.index(root)+alt)

  def isDiatonic(self, key):
    test = True
    if self.index not in key.getNotesIndex():
      return False
    return test
               
  def transpose(self,interval,sign = ''):  
    if not sign:
      sign = self.sign
    self.__init__(self.index+interval,sign)
    return self
    
    
  def format(self):
    return self.name.replace('b','♭')
    
  def __str__(self):
    return f"{self.name}"
