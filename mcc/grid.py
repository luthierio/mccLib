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
import frontmatter
import re
import sys
import os
    
from mcc.note import Note
from mcc.chord import Chord
from mcc.key import Key
from mcc.tools import *

class Grid: 
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
    lines = []
    if isinstance(section, list):
      for line in section:
        lines.append(self.parseLine(line))
    elif isinstance(section, str):
      lines.append(self.parseLine(section))
    return lines
      
  def parseLine(self,line):
    measures = []
    for measure in re.split(r'\||\║|\{|\}', line):
      if measure and measure.strip():
        measures.append(mccMeasure(measure)) 
    return measures
        
  def transpose(self,interval):  
    self.key.transpose(interval)
    self.src['key'] = self.key.name
    
    for name, section in self.grid.items():
      for line in section:
        for measure in line:
          for chord in measure.chords:
            chord.transpose(interval, self.key.sign)
    return self
          
  def yamlify(self):
    sections = {}
    for name, section in self.grid.items():
      sections[name] = []
      for line in section:
        lineTxt = '|'
        for measure in line:          
          lineTxt += measure.__str__()+'|'
        lineTxt = lineTxt.replace("|:","{:").replace(":|",":}")
        sections[name].append(lineTxt)
    return sections
  
  def saveTo(self,path):
    with open(path, "w") as file:
      file.write(self.__str__())
    return self
    
  def __str__(self):
    dist = self.src
    dist['grid'] = self.yamlify()
    return yaml.dump(dist, default_flow_style=False,allow_unicode=True, sort_keys=False,indent=True)
      
#****************
# Measure Class

class mccMeasure:

  def __init__(self, measure,beats = 2):
    self.src = measure.strip()
    self.measure = measure.strip()
    self.chords = []  
    self.beats = beats
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
      self.coda = re.search('\d+', self.measure).group(0)
      self.measure = self.measure.replace(self.coda,'').strip()      
    
    for chord in self.measure.split() :
      if chord.strip() == '÷' :
        self.repeat = True
      elif chord.strip():
        self.chords.append(Chord(chord.strip()))
    
  def __str__(self):
    txtMeasure = ''
    if self.repeatStart:
      txtMeasure += ':'
    elif self.coda:
      txtMeasure += f'{self.coda}'
    else:
      txtMeasure += ' '
      
    txtMeasure += ' '
      
    if self.repeat:
      txtMeasure += '÷'
      for x in range(0, self.beats):
        txtMeasure += '   '
    else:
      for chord in self.chords :
        txtMeasure += chord.__str__()+' '
      if len(self.chords) < self.beats:
        for x in range(len(self.chords), self.beats):
          txtMeasure += '   '
      
    if self.repeatEnd:
      txtMeasure += ':'
    else:
      txtMeasure += ' '
    return txtMeasure
   
