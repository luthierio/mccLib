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
    
from .Note import Note
from .Chord import Chord
from .Key import Key
from .Tools import *

lineSplit = r'[\|\║\{\}]\s*[\|\║\{\}]'
measureSplit = r'[\|\║\{\}]'

class mccFile: 
  def __init__(self, yamlGrid):
    self.raw = yamlGrid 
    self.src = yaml.safe_load(yamlGrid)
    self.key = Key(self.src['key'])
    self.grid = self.parseMcc(self.src['grid'])
      
  def parseMcc(self,mcc):
    grid = {}
    if isinstance(mcc, dict):
      for name, section in mcc.items():
        grid[name]= self.parseSection(section)
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
        measures.append(mccMeasure(measure, self.key)) 
    return measures
        
  def transpose(self,interval): 
    self.key.transpose(interval)
    self.src['key'] = self.key.name
    for name, section in self.grid.items():
      for line in section['lines']:
        for measure in line:
          for chord in measure.chords:
            chord.transpose(interval, self.key.sign)
    return self
          
  def yamlify(self):
    sections = {}
    for name, section in self.grid.items():
      grid = ''  
      for line in section['lines']:
        lineTxt = '|'
        for measure in line:          
          lineTxt += measure.__str__()+'|'
        lineTxt = lineTxt.replace("|:","{:").replace(":|",":}")
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
    
  def getNonDiatonicChords(self):
    nonDiatonic = []
    literalChords = [] #Used to include only once each chord in array
    for name, section in self.grid.items():
      for line in section['lines']:
        for measure in line:     
          for chord in measure.chords:  
            if not chord.isDiatonic() and chord.literal not in literalChords:
              nonDiatonic.append(chord)
              literalChords.append(chord.literal)
    return nonDiatonic      
    
  def __str__(self):
    dist = dict(self.src)
    del dist['grid']    
    result = yaml.dump(dist, default_flow_style=False,allow_unicode=True, sort_keys=False)
    result += yaml.dump({'grid':self.yamlify()}, default_style='|', sort_keys=False,allow_unicode=True, default_flow_style=False,indent=True, width=float("inf"))
    
    return result
      
#****************
# Measure Class

class mccMeasure:

  def __init__(self, measure,key = Key(),beatsNum = 2):
    self.key = key
    self.literal = measure.strip()
    self.measure = measure.strip()
    self.chords = []  
    self.beats = []  
    self.beatsNum = beatsNum
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
      self.measure = self.measure.replace(str(self.coda),'').strip()      
    
    if self.measure.strip() == '÷':
      self.repeat = True;
    else:
      for beat in self.measure.split() :
        theBeat = Beat(beat.strip(), self.key)
        self.beats.append(theBeat)
        
        if theBeat.isChord:
          self.chords.append(theBeat.chord)
    
  def __str__(self):
  
    max_beat_lenght = 10
    
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
  def __init__(self, literal, key = Key()):
      
    self.literal = literal
    self.isChord = False
    self.isRepeat = False
    self.isBreak = False
    
    if self.literal == '÷' :
      self.isRepeat = True
      
    elif self.literal == '.' or self.literal == '-' : #Repeat Beat
      self.isBreak = True
      
    elif self.literal:
      self.isChord = True
      self.chord = Chord(self.literal, key)
    
  def __str__(self):
    if self.isChord:
      return self.chord.__str__()
    else:
      return self.literal
   
