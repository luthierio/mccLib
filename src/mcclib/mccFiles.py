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
import pprint
prettyPrint = pprint.PrettyPrinter(indent=4)
import yaml
from yaml.representer import SafeRepresenter

class folded_unicode(str): pass
class literal_unicode(str): pass

def folded_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')
def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')

yaml.add_representer(folded_unicode, folded_unicode_representer)
yaml.add_representer(literal_unicode, literal_unicode_representer)

from collections import namedtuple
import re
import sys
import os
    
from .Notes import Note
from .Chords import Chord
from .Scales import Scale
from .Keys import Key
from .Tools import *

lineSplit = r'[\|\║\{\}]\s*[\|\║\{\}]'
measureSplit = r'[\|\║\{\}]'

class mccFile: 
  def __init__(self, yamlGrid):
    self.raw = yamlGrid 
    self.src = yaml.safe_load(yamlGrid)
    
    self.key = Key(self.src['key'])  
    if 'mode' in self.src:
      self.scale = Scale(self.src['key'],self.src['mode'])
      print(self.scale)
    else:
      self.scale = Scale(self.src['key'])
      
    self.grid = self.parseMcc(self.src['grid'])
      
  def parseMcc(self,mcc):
    grid = {}
    if isinstance(mcc, dict):
      for name, section in mcc.items():
        grid[name]= self.parseSection(section)
    elif isinstance(mcc, str):
      grid[''] = self.parseSection(mcc)
    return grid
    
  def parseSection(self,section):
    aSection = {
      'key':None,
      'lines': [],
    }
    
      
    if isinstance(section, list):
      for line in section:
        aSection.lines.append(self.parseLine(line))
    elif isinstance(section, str):
      if re.search(lineSplit, section):
        for line in re.split(lineSplit, section):
          aSection['lines'].append(self.parseLine(line))
      else:
        aSection['lines'].append(self.parseLine(section))
    elif isinstance(section, dict) and 'key' in section:
      aSection['key'] = Key(section['key'])
      
      key = self.key #stockage
      self.key = Key(section['key'])
      aSection['lines'] = self.parseSection(section['grid'])['lines']
      aSection['key'] = self.key
      self.key = key
      
    return aSection
      
  def parseLine(self,line):
    line = line.replace("{","|").replace("}","|") #Simplify
    measures = []
    for measure in re.split(measureSplit, line):
      if measure and measure.strip():
        measures.append(mccMeasure(measure, key = self.key, context = self)) 
    return measures
        
  def transpose(self,interval): 
    self.key.transpose(interval)
    self.src['key'] = self.key.name
    for name, section in self.grid.items():
      key = self.key
      if section['key']:
        key = section['key'].transpose(interval)
      for line in section['lines']:
        for measure in line:
          for chord in measure.chords:
            chord.transpose(interval, key.sign)
    return self
          
  def yamlify(self):
    sections = {}
    for name, section in self.grid.items():
      grid = ''  
      for line in section['lines']:
        lineTxt = '|'
        for measure in line:          
          lineTxt += measure.__str__()+'|'
        grid += literal_unicode(u''+lineTxt+'\n')

      if section['key'] != None:
        sections[name] =  {'key':section['key'].literal,'grid':grid}
        #print(self.src['name'], name, sections[name])
      else:
        sections[name] = grid    
      
    return sections
  
  def saveTo(self,path):
    with open(path, "w") as file:
      file.write(self.__str__())
    return self
    
  def getAnalysis(self):
    analysis = {
      'sections':{},
      'keys':{},
      'nonDiatonicChords':{},
    }
    for name, section in self.grid.items():
      key = section['key'] if section['key'] else self.key
      analysis['sections'][name] = {
        'key':key,
        'nonDiatonicChords':{},
      }
      if key.name not in analysis['keys']:
        analysis['keys'][key.name] = {
          'key': key,
          'nonDiatonicChords':{},
        }
      for line in section['lines']:
        for measure in line:     
          for chord in measure.chords:  
            if not chord.isDiatonic():
              analysis['sections'][name]['nonDiatonicChords'][chord.literal] = chord
              analysis['keys'][key.name]['nonDiatonicChords'][chord.literal] = chord
              analysis['nonDiatonicChords'][chord.literal] = chord
    return analysis    
    
  def __str__(self):
    dist = dict(self.src)
    del dist['grid']    
    result = yaml.dump(dist, default_flow_style=False,allow_unicode=True, sort_keys=False)
    result += yaml.dump({'grid':self.yamlify()}, default_style='|', sort_keys=False,allow_unicode=True, default_flow_style=False,indent=True, width=float("inf"))
    
    return result
      
#****************
# Measure Class

class mccMeasure:

  def __init__(self, measure,**options):  
  
    default = {'key':Key(),'beatsNum':2}
    self.options = {**default, **options}
      
    self.key = self.options['key']
    self.context = self.options['context']
    self.beatsNum = self.options['beatsNum']
    
    self.literal = measure.strip()
    self.measure = measure.strip()
    self.chords = []  
    self.beats = []  
    self.coda = False
    self.repeat = False
    self.repeatStart = False
    self.repeatEnd = False
    
    if self.measure.startswith(':'):
      self.repeatStart = True;   
    if self.measure.endswith(':'):
      self.repeatEnd = True;   
    self.measure = self.measure.replace(':','').replace(':','').strip()
    
    if re.match('\d+', self.measure):
      self.coda = int(re.search('\d+', self.measure).group(0))
      self.measure = self.measure[1:]     
    
    if self.measure.strip() == '÷':
      self.repeat = True;
    else:
      for beat in self.measure.split() :
        theBeat = Beat(beat.strip(), key = self.key, context = self.context)
        self.beats.append(theBeat)
        
        if theBeat.isChord:
          self.chords.append(theBeat.chord)
    
  def __str__(self):
  
    max_beat_lenght = 12
    
    txtMeasure = ''
    if self.repeatStart:
      txtMeasure += ':'
    elif self.coda:
      txtMeasure += f'{self.coda}'
    else:
      txtMeasure += ' '
      
    txtMeasure += ' '
      
    if self.repeat:
      txtMeasure += '÷ '
      for x in range(0, self.beatsNum):
        txtMeasure += ' '*(max_beat_lenght)
    else:
      for beat in self.beats :
        txtMeasure += beat.__str__()+' '
        for x in range(len(beat.__str__()), max_beat_lenght):
          txtMeasure += ' '
      if len(self.beats) < self.beatsNum:
        for x in range(len(self.beats), self.beatsNum):
          txtMeasure += ' '*(max_beat_lenght+1)
      
    if self.repeatEnd:
      txtMeasure += ':'
    else:
      txtMeasure += ' '
    return txtMeasure
    
#****************
# Beat Class

class Beat:
  def __init__(self, literal, **options):

    default = {'key':Key()}
    self.options = {**default, **options}      
    self.key = self.options['key']  
    self.context = self.options['context']
          
    self.literal = literal
    self.isChord = False
    self.isRepeat = False
    self.isBreak = False
    
    if self.literal == '÷' :
      self.isRepeat = True
      
    elif self.literal == '.' or self.literal == '-' : #Repeat Beat
      self.isBreak = True
      
    elif self.literal.replace('(','').replace(')',''):
      self.isChord = True
      self.chord = Chord(self.literal.replace('(','').replace(')',''), key = self.key, context = self.context)
    
  def __str__(self):
    if self.isChord:
      return self.chord.__str__()
    else:
      return self.literal
   
