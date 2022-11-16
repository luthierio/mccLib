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


noteNames = ["C","","D","","E","F","","G","","A","","B"]

class Note:
  
  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, note, sign = ''):
    
    self.sign =  sign
    
    self.root = '' #Si altération, la racine de la note: C#, root = C
    self.name = ''
    self.temperName = ''
    self.index = ''

    if isinstance(note, str):
    
      if self.sign == '' and len(note) > 1:    
        self.sign = note[1]
        
      self.index = self.getIndexFromName(note)
        
    elif isinstance(note, int):
      self.index = self.getIndexFromNum(note)
    
    self.name = self.getNameFromIndex(self.index)
  
      
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
           
  def transpose(self,interval):  
   self.__init__(self.index+interval,self.sign)
   return self
    
    
  def print(self):
    print(self,'\t',self.name)
    
  def __str__(self):
    return f"{self.name}"
