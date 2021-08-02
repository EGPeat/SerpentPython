import bitarray
from bitarray import bitarray
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("basekey", help="basekey of the function",
                    type=str)
args = parser.parse_args()
truebasekey=bitarray(args.square)
testing3=int(args.square,2)
print(testing3**2)
print(testing2)





#parser.add_argument("keyinint", help="serpent of built in words with inputted key",
#                    type=int)


