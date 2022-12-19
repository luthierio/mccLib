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
  parts = re.search('(([ABCDEFG])([b|#])?)([ A-za-z]*)?', literalKey)
  obj = {
    'tonic': parts.group(1),
    'root' : parts.group(2),
    'alt'  : parts.group(3) if parts.group(3) else '',
    'type' : parts.group(4).strip() if parts.group(4) else '' ,
  }
  return obj
  
def parseChord(literalChord):
  parts = re.search('(([ABCDEFG])([b|#])?)([A-Za-z0-90-9°øΔ+?]*)?([/][A-Z][b|#]?)?', literalChord)
  obj = {
    'root' : parts.group(1),
    'sign'  : parts.group(3) if parts.group(3) else '',
    'type' : parts.group(4).strip() if parts.group(4) else '' ,
    'bass' : parts.group(5)[1:] if parts.group(5) else '' ,
  }
  return obj
