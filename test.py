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

f = open('./src/Blue drag.mcc','r')
grid = f.read()
print(grid)
print(Grid(grid))
print(Grid(grid).transpose(2).saveTo('./dist/Blue drag.mcc (Em)'))
#Grid('./src/Blue drag.mcc').print().transpose(2).print().save('./dist/Blue drag.mcc').transpose(-2).print()


