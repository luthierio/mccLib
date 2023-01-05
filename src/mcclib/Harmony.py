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

from .Literals import parseKey, parseChord
from itertools import chain


# distance of each notes from root
# https://theoriemusicale.camilleroux.com/accords/
noteNames = ["C","","D","","E","F","","G","","A","","B"]

chordTypes = {
  "?"   :[0,7],
  ""    :[0,4,7], #Nothing specified means Major triad
  "M"   :[0,4,7],
  "M7"  :[0,4,7,11],
  "Δ"   :[0,4,7,11],
  "M6"  :[0,4,7,9],
  "69"  :[0,4,7,9,14],
  "6"   :[0,4,7,9   ],
  "9"   :[0,4,7,  14],
  "9+"  :[0,4,7,  15],
  
  "13"  :[0,4,7,  8],
  "13b9":[0,4,7,  8,13],
  
  "m"   :[0,3,7],
  "m6"  :[0,3,7,9],
  "mb6" :[0,3,7,8],
  "m7"  :[0,3,7,10],
  "mΔ"  :[0,3,7,11],
  "mΔ7" :[0,3,7,11],# A vérifier
  "m9"  :[0,3,7,14],
  "m11" :[0,3,7,5],# A vérifier
  
  "7"   :[0,4,7,10],
  "9"   :[0,4,7,10,14],
  "9b"   :[0,4,7,10,13],
  "9b5" :[0,4,6,10,14],
  "79"  :[0,4,7,10,14],
  "7b9" :[0,4,7,10,13],
  "7b13":[0,4,7,10,8],  #b13 = #5
  
  "7+"  :[0,4,8,10],# A vérifier
  "+7"  :[0,4,8,10],# A vérifier
  "7aug":[0,4,8,10],# A vérifier
  "7#5" :[0,4,8,10],# A vérifier
  "75+" :[0,4,8,10],# A vérifier
  
  "7b5" :[0,4,6,10],# A vérifier
  
  "7sus" :[0,5,7,10],# A vérifier
  "7sus4":[0,5,7,10],# A vérifier
  
  "°"   :[0,3,6,9],
  "0"   :[0,3,6,9],
  "dim" :[0,3,6,9],
  
  "m7b5":[0,3,7,9],
  "ø"   :[0,3,7,9],
  
  "+"   :[0,4,8],
  "+Δ"  :[0,4,8,11],
  "5+"  :[0,4,8],
  "aug" :[0,4,8],
  
  "5+11+"  :[0,4,8,6],
  #"3b9"  :[0,1,2,3,4,5,6,7,8,9,10,11],
}  



majorScale              = {
  'intervals' : [2    ,2    ,1    ,2    ,2    ,2    ,1    ], 
  'chords'    : ['Δ'  ,'m7' ,'m7' ,'Δ'  ,'7'  ,'m7' ,'ø'  ],
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
  'chords'    : ['mΔ' ,'ø'  , '+Δ' ,'m7' ,'7' ,None  ,None   ,'Δ'   ,'°'  ],
}

#('minor harmonic', 5)
def buildMode(model, degree=1):
  index = degree-1
  newModel = {
    'intervals':model['intervals'][index:] + model['intervals'][:index],
    'chords':model['chords'][index:] + model['chords'][:index],
  }
  return newModel

Abbrv = {
  '':'major',
  'M':'major',
  'm':'minor',
  '7':'superphrygien',
  'mh':'minor harmonic',
  'mm':'minor melodic',
  'mn':'minor natural',
}
scaleModels = {
  'major': majorScale,
  'minor': minorScale,
  
  'minor harmonic': minorHarmonicScale,
  'minor melodic': minorMelodicScale,
  'minor natural' : minorNaturalScale,  
  'eolien': minorNaturalScale,
  
  'superphrygien' : buildMode(minorHarmonicScale,5),
  
  'test' : buildMode(majorScale,1),
}

#################################
# Notes
#

class Note:
  
  #Note is a integer from 0 to 11 or a name C#... sign force use of 'b' or '#' to name unamed notes
  def __init__(self, note, context = None):
    
    from .Harmony import Scale, Chord
    
    self.context = context
    self.sign = ''
    if isinstance(context, Key):
      self.sign =  context.sign
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
    if self.index not in key.notesIndex():
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
    
  def __repr__(self):
    return f"{self.name}"

#################################
# Key
#
class Key:
  
  #key is a note
  def __init__(self, key = None, **options):
  
    default = {'simplify':True}
    options = {**default, **options}
    
    if not key:
      key = 'C'
      
    if isinstance(key, str):
      keyParts = parseKey(key)
      self.name = key
      self.literal = key
      self.tonic = Note(keyParts['tonic']) 
      self.sign = keyParts['alt']
      self.type = keyParts['type']
    elif isinstance(key, Note):
      self.name = key.name
      self.literal = key.name
      self.tonic = key 
      self.sign = key.sign    
      self.type = ''  
      
    
    if self.type in Abbrv:
      self.type = Abbrv[self.type]
    
    if self.type == 'minor':
      self.relative = Note(self.tonic.name).transpose(+3)
    else:
      self.relative = Note(self.tonic.name).transpose(-3)
      
    if options['simplify']:
      self.simplifyKey()  

    self.scale = Scale(self)      
    self.signature = Signature(self)
    self.sign = self.signature.sign
    
  def simplifyKey(self):
    #lors des transpositions, certains choix sont posés pour éviter des armures trop complexes
    equiv = {
      'Fb':'E', #oublier Fab
      'E#':'F', #oublier Mi#
      'B#':'C', #oublier Si#
      'Cb':'B', #oublier Dob
    }
    for fromkey, tokey in equiv.items():
      if self.tonic.name == fromkey:
        self.tonic = Note(tokey)
        self.__init__(self.tonic.name+self.type)
    
    if self.type =='minor': 
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
      if self.tonic.name == fromkey:
        self.tonic = Note(tokey)
        self.__init__(self.tonic.name+self.type)
    return self
    
  def transpose(self,interval):
    self.tonic.transpose(interval)
    self.__init__(self.tonic.name+self.type)
    return self
          
  def scale(self):
    return Scale(self)  
         
  def notes(self):
    return Scale(self).notes()          
      
  def notesIndex(self):
    indexes = []
    for note in self.notes():
      indexes.append(note.index)
    return indexes  

  def scales(self):
    scales = []
    if self.type == 'minor':
      scales.append(Scale(Key(self.tonic.name+'mh'))) #Mineur harmonique
      scales.append(Scale(Key(self.tonic.name+'mm'))) #Mineur mélodique
    else:
      scales.append(Scale(self)) #Majeur
    return scales
  '''      
  def consonant():
    notes = []
    return notes

  def dissonant():
    notes = []
    return notes     
  '''        
  def abbrv(self):
    for abbrv, atype in Abbrv.items():
      if self.type == atype:
        return abbrv
    return self.type
    
  def print(self):
    print(self,'\t',self.tonic.name,'\t',self.type,'\t',self.name,'\t',self.sign,'\t',self.notesNames)
    
  def __str__(self):
    if self.type in Abbrv:
      return f"{self.tonic} " + Abbrv[self.type]
    elif not self.type:
      return f"{self.tonic} major"
    else:
      return f"{self.tonic} {self.type}"

  def __repr__(self):
    return f"{self.__str__()}"
#################################
# Chords
#

class Chord:

  #Note is a integer from 0 to 11 or a name C#... context force use of 'b' or '#' to name unamed notes
  def __init__(self, chord, key = None):
      
    self.key = Key()
    self.sign = ''        
    self.name = ''
    self.root = ''
    self.alt = ''
    self.type = ''
    self.bass = ''
    self.intervals = []
    self.notesNames = []
    
    if isinstance(key, Key):
      self.sign = key.sign
      self.key = key
    
    if isinstance(chord, str):
      self.literal = chord
      parts = parseChord(chord)
      self.sign = parts['sign'] if parts['sign'] else self.sign      
      self.root = Note(parts['root'],self)
      self.bass = Note(parts['bass'],self) if parts['bass'] else ''      
      self.type = parts['type']
      if self.type == '?':
        self.floating = True
    else:
      raise ValueError(chord," n'est pas un type d'accord valable")

    if self.type not in chordTypes:  
      raise ValueError(self.type," n'est pas un type de d'accord connu")
    self.intervals = chordTypes[self.type] 
    self.notesNames = self.getNotesNames()
        
      
  def transpose(self, interval, sign = ''):
  
    self.root.transpose(interval, sign)
    if self.bass:
      self.bass.transpose(interval, sign)
    self.__init__(self.__str__())
    
    return self
  
  def notes(self):
    notes = []
    if isinstance(self.bass,Note):
      notes.append(self.bass)
    for interval in self.intervals:
      note = Note(self.root.index+interval,self)
      notes.append(note)
    return notes
    
  def getNotesNames(self):
    names = []
    for note in self.notes():
      names.append(note.name)
    return names 
    
  def isDiatonic(self):
  
    diatonicNotes = []
    test = True
    if isinstance(self.key, Key):
      diatonicNotes = self.key.notes()
      indexes = []
      for note in diatonicNotes:
        indexes.append(note.index)      
      for note in self.notes():
        if note.index not in indexes:
          return False
    return test
    
  def consonant(self):
    notes = []    
    indexes = []    
    for note in self.notes():
      if note.index in self.key.notesIndex() and note.index not in indexes:
        notes.append(note)
        indexes.append(note.index)
    return notes

  def dissonant(self):
    notes = []    
    indexes = []   
    for note in self.notes():
      if note.index not in self.key.notesIndex() and note.index not in indexes:
        notes.append(note)
        indexes.append(note.index)
    return notes
    
  def print(self):
    print(self,'\t',self.type,'\t',self.bass,'\t',self.intervals,'\t',self.notesNames)
    
  def __str__(self):
  
    if self.bass:
      return self.root.name+self.type+'/'+self.bass.name
    else:
      return self.root.name+self.type

  def __repr__(self):
    return f"{self.__str__()}"        


#################################
# Scales
#
    
class Scale:
  def __init__(self, key, mode = False):
  
      self.key = key
      if not isinstance(self.key, Key): 
        raise ValueError(self.key," n'est pas une toanlité")
      
      self.model = scaleModels[self.key.type]        
      
  def notes(self):
      # Génération des notes de la gamme en fonction de sa tonique et de son mode
      # Retourne un tableau de notes de la gamme
      notes = []
              
      index = 0
      for interval in self.model['intervals']:
        note = Note(self.key.tonic.index+index, self.key)
        index = index+interval
        notes.append(note)  
      return notes

  def chords(self):
      #harmonize
      # Génération des accords de la gamme en fonction de sa tonique et de son mode
      # Retourne un tableau d'accords de la gamme 
      chords = [] 
      for i, note in enumerate(self.notes()):
        if self.model['chords'][i]:
          #le test permet de ne pas harmoniser si None
          chord = Chord(note.name+self.model['chords'][i], self.key)
          chords.append(chord)  
      return chords

  def __str__(self):
    return f"{self.key}"           

  def __repr__(self):
    return f"{self.__str__()}"      

class Signature:

  #Note is a note, type is 'm' or '' (=M) or 'M'
  def __init__(self, key):
    
    self.sign = key.sign
    
    if isinstance(key, str): 
      self.key = Key(key)
    elif isinstance(key, Key):   
      self.key = key              
        
    if self.key.abbrv() == '': #Tonalité majeure
    
      if self.key.tonic.name in ["F"]: 
        self.sign = 'b'
      elif self.key.tonic.name in ["G","D","A","E","B"]: 
        self.sign = '#'  

    else: #Une des tonalités mineures
    
      if self.key.tonic.name in ["F","C","G","D"]: 
        self.sign = 'b'
      elif self.key.tonic.name in ["E","B"]: 
        self.sign = '#'  

  def __str__(self):
    return f"{self.sign}"           

  def __repr__(self):
    return f"{self.__str__()}"      
              
