import random
import bitarray
from bitarray import bitarray
from bitarray.util import hex2ba
import secrets


for i in range(0,20):
    basekey=bitarray()
    for i in range(0,256):
            x = random.randint(0, 1)
            basekey.append(x)
    print("Basekey",basekey)
    print("Basekey Count",basekey.count(1))


lordno=secrets.token_hex(32)
lordno=hex2ba(lordno)
print("lordno",lordno)
print("lordno count",lordno.count(1))
