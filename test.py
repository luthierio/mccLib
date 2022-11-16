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
from mcc.note import Note
from mcc.chord import Chord

Chord('Am').print()
Chord('Am6').print()
Chord('Am7').print()
Chord('A').print()
Chord('A/C').print()
Chord('A7').print()
Chord('Am7b5').print()
Chord('A°').print()
Chord('Adim').print()
Chord('CM7').print()
Chord('C69').print()
Chord('Ab').print()
Chord('Abm6').print()
Chord('Abm6').transpose(1).print()
Chord('Abm6').transpose(-149).print()


"""
aNote = Note('C')
print("C = ",aNote)

aNote = Note('C').shift(2)
print("C+2 = ",aNote)

aNote = Note('C#')
print("C# = ",aNote)


aNote = Note('Cb')
print("Cb = ",aNote)
aNote = Note('Cbb')
print("Cbb = ",aNote)
aNote = Note('Cbb','b')
print("Cbb(b) = ",aNote)
aNote = Note('Cbb','#')
print("Cbb(#) = ",aNote)

aNote = Note('B#')
print("B# = ",aNote)
aNote = Note('B##')
print("B## = ",aNote)
aNote = Note('B##','b')
print("B##(b) = ",aNote)
aNote = Note('B##','#')
print("B##(#) = ",aNote)

aNote = Note(0)
print("0 = ",aNote)
aNote = Note(1)
print("1 = ",aNote)
aNote = Note(1,'b')
print("1(b) = ",aNote)
aNote = Note(11)
print("11 = ",aNote)
aNote = Note(11,'b')
print("11(b) = ",aNote)

aNote = Note(2)
print("2 = ",aNote)
"""
