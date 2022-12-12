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

import re

def parseKey(literalKey):
  keyParts = re.search('(([ABCDEFG])([b|#])?)([mM])?', literalKey)
  obj = {
    'tonic': keyParts.group(1),
    'root' : keyParts.group(2),
    'alt'  : keyParts.group(3) if keyParts.group(3) else '',
    'type' : keyParts.group(4) if keyParts.group(4) else '' ,
  }
  return obj
