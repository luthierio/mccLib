# mccLib

mccLib is a python library use to manipulate (transpose, parse and print) musical chords charts in MCC format.

It can be use to manipulate Notes, Keys, Chords, Signature, Scales.

```python
from mcclib import *
aKey = Key('Gm')
print(aKey.notes())
#Result: [G, A, Bb, C, D, Eb, E, F, Gb]
print(aKey.scales())
#Result: [G minor harmonic, G minor melodic]
print(aKey.scale.chords())
#Result: [GmΔ, Aø, Bb+Δ, Cm7, D7, FΔ, Gb°]
```



