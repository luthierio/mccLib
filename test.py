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

from mcc.note import Note
from mcc.chord import Chord
from mcc.key import Key
from mcc.tools import *
from mcc.grid import Grid
from pathlib import Path

Path('./test/dist/Bb/').mkdir(parents=True, exist_ok=True)
Path('./test/dist/Eb/').mkdir(parents=True, exist_ok=True)
Path('./test/dist/src/').mkdir(parents=True, exist_ok=True)

files = Path('./test/src/').glob('*.mcc')
for file in files:
  theGrid = Grid(file.read_text())
  theGrid.transpose(2).saveTo('./test/dist/Bb/'+theGrid.src['name']+' ('+theGrid.key.name+').mcc')
  theGrid.transpose(-3).saveTo('./test/dist/Eb/'+theGrid.src['name']+' ('+theGrid.key.name+').mcc')

files = Path('./test/dist/Bb/').glob('*.mcc')
for file in files:
  theGrid = Grid(file.read_text())
  theGrid.transpose(-2).saveTo('./test/dist/src/'+theGrid.src['name']+' ('+theGrid.key.name+').mcc')

