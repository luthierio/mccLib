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
from .Notes import Note
from .Signatures import Signature

majorScale              = {
  'intervals' : [2    ,2    ,1    ,2    ,2    ,2    ,1      ], 
  'chords'    : ['M7' ,'m7' ,'m7' ,'M7' ,'7'  ,'m7' ,'m7b5' ],
}
#majorIntervals          = [0,2,2,1,2,2,2,1]#Taille des intervalles
#majorChords             = ['M7','m7','m7','M7','G7','m7','m7b5']

minorNaturalScale       = {
  'intervals' : [2    ,1    ,2    ,2    ,1    ,2    ,1      ], 
  'chords'    : ['m7' ,'ø'  , 'Δ' ,'m7' ,'m7' ,'Δ'  ,'7'    ],
}

minorHarmonicScale       = {
  'intervals' : [2    ,1    ,2    ,2    ,1    ,3    ,1      ], 
  'chords'    : ['mΔ' ,'ø'  ,'+Δ' ,'m7' ,'7'  ,'Δ'  ,'°'    ],
}

minorMelodicScale       = {
  'intervals' : [2    ,1    ,2    ,2    ,2    ,2    ,1      ], 
  'chords'    : ['mΔ' ,'m7' ,'+Δ' ,'7'  ,'7'  ,'ø'  ,'ø'    ],
}
minorScale       = {
  'intervals' : [2    ,1    ,2    ,2    ,1    ,1    ,1    ,1    ,1    ], 
  'chords'    : ['m7' ,'ø'  , 'Δ' ,'m7' ,'m7' ,'Δ'  ,'ø'  ,'7'  ,'°'  ],
}

#('minor harmonic', 5)
def buildMode(model, degree=1):
  index = degree-1
  newModel = {
    'intervals':model['intervals'][index:] + model['intervals'][:index],
    'chords':model['chords'][index:] + model['chords'][:index],
  }
  return newModel

scaleAbrv = {
  'M':'major',
  'm':'minor',
  'mh':'minor harmonic',
  'mm':'minor melodic',
  'mn':'minor natural',
}
scaleModels = {
  'major': majorScale,
  'minor': minorScale,
  
  'minor harmonic': minorHarmonicScale,
  'minor melodic': minorMelodicScale,
  
  'eolien': minorNaturalScale,
  'minor natural' : minorNaturalScale,
  'superphrygien' : buildMode(minorHarmonicScale,5),
  'test' : buildMode(majorScale,2),
}


# Scale(Note('C'))
# Scale('C')
# Scale('Cm')
# Scale('Cm', 'harmonic')
# Scale('C' , 'mh')
    
class Scale:
    def __init__(self, *args, **options):
        # Traitement des arguments positionnels dans args
        self.args = args

        # Traitement des arguments nommés dans kwargs
        self.options = options   

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
            self.type = self.args[0][2:].strip()
          # Scale('Cm')
          else:
            self.tonic = Note(self.args[0][0])
            self.type = self.args[0][1:].strip()
          
          
        if len(self.args) > 1 and isinstance(self.args[1], str):
          self.type = self.args[1]
            
        if not hasattr(self, "type") or self.type == '':
          self.type = 'major'
        
        if self.type in scaleAbrv:
          self.type = scaleAbrv[self.type]
        
        if self.type not in scaleModels:  
          raise ValueError(self.type," n'est pas un type de gamme valable")
        self.model = scaleModels[self.type]
        
        #TODO comment déterminer si armature en diez ou bémol si je pense une gamme autre que major ou minor?????  
        self.signatureType = '' if self.type== 'major' else 'm'
        self.signature = Signature(self.tonic,self.signatureType)
        
    def notes(self):
        # Génération des notes de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau de notes de la gamme
        notes = []
        
        index = 0
        for interval in self.model['intervals']:
          note = Note(self.tonic.index+index, self)
          #print(self.tonic.index,index, note.index)
          index = index+interval
          notes.append(note)  
        return notes

    def chords(self):
        #harmonize
        from .Chords import Chord
        from .Keys import Key
        # Génération des accords de la gamme en fonction de sa tonique et de son mode
        # Retourne un tableau d'accords de la gamme 
        chords = [] 
        for i, note in enumerate(self.notes()):
          chord = Chord(note.name+self.model['chords'][i], self)
          chords.append(chord)  
        return chords

    def __str__(self):
      return f"{self.tonic.name} {self.type}"     
