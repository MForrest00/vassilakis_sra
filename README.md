## Vassilakis SRA (Spectral and Roughness Analysis)

### Introduction

This package contains a simple implementation of the SRA (Spectral and Roughness Analysis) model described here: http://www.acousticslab.org/learnmoresra/moremodel.html  
The model was developed by Pantelis Vassilakis. You can find more information here: http://www.acousticslab.org/

### Installation

`pip install vassilakis_sra`

### Contents

This package contains three entities which represent the components of the Vassilakis SRA model.

1. `Sinusoid` - a simple representation of a sinusoid
    + Includes a value for frequency and a value for amplitude
2. `SRACalculation` - a module singleton which represents the Vassilakis SRA calculation
3. `SRAModel` - a stateful implementation of the calculation in `SRACalculation`
    + An instance of this model will contain the current roughness value, the sinusoids used to calculate that value, and the contributions to the total roughness value of each sinusoid and sinusoid pair.
    + Instances will offer methods to add sinusoids to or remove sinusoids from the current model, test impact of adding or removing sinusoids (without actually changing model state), and interrogate contributions of sinusoids and sinusoid pairs to the total roughness value. 

### Examples

To create a `Sinusoid`:

```
from vassilakis_sra import Sinusoid`

s1 = Sinusoid(440.0, 1.0)
s2 = Sinusoid(frequency=466.1638, amplitude=2.0)
```

To generate a roughness value:
```
from vassilakis_sra import Sinusoid, SRACalculation

s1 = Sinusoid(440.0, 1.0)
s2 = Sinusoid(frequency=466.1638, amplitude=2.0)

roughness_data = SRACalculation([s1, s2])
```

To generate a roughness value without instantiating `Sinusoid` objects:
```
from vassilakis_sra import SRACalculation

s1 = Sinusoid(440.0, 1.0)
s2 = Sinusoid(frequency=466.1638, amplitude=2.0)

roughness_data = SRACalculation([(440.0, 1.0), (466.1638, 2.0)])
```

