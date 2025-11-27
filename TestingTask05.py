import numpy
from functools import reduce
import operator

bits = numpy.random.randint(0,2,16)
print(bits)

print(reduce(operator.xor,[i for i,bit in enumerate(bits) if bit]))
