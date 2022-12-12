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
from itertools import chain
from .Note import Note
from .Signature import Signature

majorScale              = [0,2,4,5,7,9,11] #Numéro de notes
majorIntervals          = [0,2,2,1,2,2,2,1]#Taille des intervalles
majorChords             = ['M7','m7','m7','M7','G7','m7','m7b5']

minorNaturalScale       = [0,2,3,5,7,8,10]#Numéro de notes
minorHarmonicScale      = [0,2,3,5,7,8,11]#Numéro de notes
minorMelodicScale       = [0,2,3,5,7,9,11]#Numéro de notes
minorScale              = list(set(list(chain(minorNaturalScale, minorHarmonicScale, minorMelodicScale))))#set permet de supprimmer les doublons

minorNaturalIntervals   = [0,2,1,2,2,1,2,2]#Taille des intervalles
minorHarmonicIntervals  = [0,2,1,2,2,1,3,1]#Taille des intervalles
minorMelodicIntervals   = [0,2,1,2,2,2,2,1]#Taille des intervalles

minorNaturalChords  = ['m7','ø' , 'Δ' ,'m7' ,'m7' ,'Δ'  ,'7']
minorHarmonicChords = ['mΔ','ø' ,'+Δ' ,'m7' ,'7'  ,'Δ'  ,'°']
minorMelodicChords  = ['mΔ','m7','+Δ' ,'7'  ,'7'  ,'ø'  ,'ø']

scaleAbrv = {
  'M':'major',
  'm':'minor'
}
scaleTypes = {
  'major': majorScale,
  'minor': minorScale,
  
  'minor harmonic': minorHarmonicScale,
  'minor melodic': minorMelodicScale,
  
  'eolien': minorNaturalScale,
  'minor natural' : minorNaturalScale,
}

# Scale('C')
# Scale('Cm')
# Scale('Cm', 'harmonic')
# Scale('C' , 'eolien')
    
class Scale:
    def __init__(self, *args, **kwargs):
        # Traitement des arguments positionnels dans args
        self.args = args

        # Traitement des arguments nommés dans kwargs
        self.kwargs = kwargs   

        if isinstance(self.args[0], Note): 
          # Scale(Note('C'))
          self.tonic = self.args[0]
        elif isinstance(self.args[0], str) and len(self.args[0]) == 1:  
          # Scale('C')
          self.tonic = Note(self.args[0])
        elif isinstance(self.args[0], str) and len(self.args[0]) >= 2:  
          # Scale('Cbm')
          if self.args[0][1] in  ["b","#"]:          
            self.tonic = Note(self.args[0][:2])
            self.name = self.args[0][2:].strip()
          # Scale('Cm')
          else:
            self.tonic = Note(self.args[0][0])
            self.name = self.args[0][1:].strip()
          
          
        if len(self.args) > 1 and isinstance(self.args[1], str):
          self.name = self.args[1]
            
        if not hasattr(self, "name") or self.name == '':
          self.name = 'major'
        
        if self.name in scaleAbrv:
          self.name = scaleAbrv[self.name]
        
        if self.name not in scaleTypes:  
          raise ValueError(self.name," n'est pas un type de gamme valable")
        
        self.type = '' if self.name == 'major' else 'm'
        #TODO comment déterminer si armature en diez ou bémol si je pense une gamme autre que major ou minor?????  
        self.signature = Signature(self.tonic,self.type)
        
    def notes(self):
        # Génération des notes de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau de notes de la gamme
        notes = []
        
        for noteNum in scaleTypes[self.name]:
          note = Note(self.tonic.index+noteNum, self.signature.sign)
          notes.append(note)  
        return notes

    def chords(self):
        # Génération des accords de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau d'accords de la gamme 
        chords = []
                
'''        
    def intervals(self):
        # Génération des intervalles de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau d'intervalles de la gamme

    def chords(self):
        # Génération des accords de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau d'accords de la gamme    
        
    def harmonize(self):
        # Harmonisation de la gamme en utilisant les accords générés par la méthode chords
        # Retourne une harmonisation de la gamme sous forme d'un tableau d'accords
'''
