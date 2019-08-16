## Vassilakis SRA (Spectral and Roughness Analysis)

### Introduction

This package contains a simple implementation of the SRA (Spectral and Roughness Analysis) model described here: http://www.acousticslab.org/learnmoresra/moremodel.html  
The model was developed by Pantelis Vassilakis. You can find more information here: http://www.acousticslab.org/

### Installation

`pip install vassilakis_sra`

### Contents

This package contains two entities which represent the components of the Vassilakis SRA model.

1. `Sinusoid` - a simple representation of a sinusoid
    + Includes a value for frequency and a value for amplitude.
    + Both frequency and amplitude must be an integer or float and must be greater than 0.0.
3. `SRAModel` - a stateful representation of the SRA model applied to a set of sinusoids
    + An instance of this model contains the current roughness value, the sinusoids used to calculate that value, and the contributions to the total roughness value of each sinusoid pair.
    + Instances offer methods to add sinusoids to or remove sinusoids from the current model, test impact of adding or removing sinusoids (without actually changing model state), and interrogate contributions of sinusoids and sinusoid pairs to the total roughness value. 

### Examples

To create a `Sinusoid` instance:
```python
from vassilakis_sra import Sinusoid

s1 = Sinusoid(440.0, 1.0)
s2 = Sinusoid(frequency=466.1638, amplitude=2.0)
```

To generate a roughness value from `Sinusoid` instances:
```python
from vassilakis_sra import Sinusoid, SRAModel

s1 = Sinusoid(440.0, 1.0)
s2 = Sinusoid(frequency=466.1638, amplitude=2.0)

sra = SRAModel([s1, s2])

print(sra.roughness)
```

To generate a roughness value without creating `Sinusoid` instances:
```python
from vassilakis_sra import SRAModel

sra = SRAModel([(440.0, 1.0), (466.1638, 2.0)])

print(sra.roughness)
```
Notice that the `SRAModel` class can accept a list of two-element tuples instead of `Sinusoid` objects. It can also accept a mixture of the two. Two-element tuples will be converted into `Sinusoid` objects in the `SRAModel` instance.