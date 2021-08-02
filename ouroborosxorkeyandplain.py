import sys
import bitarray
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from bitarray.util import zeros
from bitarray.util import serialize
from bitarray.util import ba2hex
from bitarray.util import make_endian


import random
import argparse
#truebasekey=[]
#parser = argparse.ArgumentParser()
#parser.add_argument("basekey", help="basekey of the function",
#                    type=str)

#parser.add_argument("filename", help="filename of file to be encrypted",
#                    type=str)
#args = parser.parse_args()
#truebasekey=bitarray(args.basekey)
#testingbasekey=int2ba(int(args.basekey,16))
#truefilename=args.filename


def extendlen(input2, output,outputlength):
    if len(input2) <outputlength:
        lengthen8multinsertfront(input2)
        while len(input2) <outputlength:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    output.append(input2)
        


#extendlen(testingbasekey,truebasekey,256)
#truebasekey=truebasekey[0]




import os
import time
start_time = time.time()


LayerPInput=[]
Player=[]
basekey=bitarray()
basekeyworking=[]
Key8wrds=[]
Key8wrdsInverse=[]
prekeyschedule=[]
prekeyscheduleInverse=[]
Key8wrdsnibble=[]
Key8wrdsnibbleInverse=[]
Key8wrdsnibblesboxes=[]
Key8wrdsnibblesboxesInverse=[]
keyschedulesboxes=[]
keyschedulesboxesInverse=[]
IP=[]
EP=[]
roundkeys=[]
SBoxKeyList=[3,2,1,0,7,6,5,4]
PlayerIPed=[]
keysboxnibbleholder=[]
keysboxnibbleholderInverse=[]
Playerinputnibble=[]
Playeroutputnibble=[]
Key8wrdspostnibble=[]
Key8wrdspostnibbleInverse=[]
tempword1=[]
tempword2=[]
tempword3=[]
tempword4=[]
SubkeysKi=[]
SubkeysKiInverse=[]
BIntermediateXORed=[]
BIntermediateBitSliced=[]
BIntermediateBitSlicedSBoxed=[]
BIntermediate32Word=[]
BIntermediate32LinMixed=[]
LayerPInputEndian=''
BIntermediate32WordBA=[]
FinalWordEndian=''
FinalWordEndianInverse=''
FinalWordEndian2=''
FinalWordEndian2Inverse=''
WordEndian=''
WordEndianInverse=''
#fracgoldratio=2644438137
fracgoldratio=bitarray('10011101100111101110110001111001')
serpentsboxes = ([   [3], [8],[15], [1],[10], [6], [5],[11],[14],[13], [4], [2], [7], [0], [9],[12]],
                  [ [15],[12], [2], [7], [9], [0], [5],[10], [1],[11],[14], [8], [6],[13], [3], [4]],
                  [  [8], [6], [7], [9], [3],[12],[10],[15],[13], [1],[14], [4], [0],[11], [5], [2]],
                  [  [0],[15],[11], [8],[12], [9], [6], [3],[13], [1], [2], [4],[10], [7], [5],[14]],
                  [  [1],[15], [8], [3],[12], [0],[11], [6], [2], [5], [4],[10], [9],[14], [7],[13]],
                  [ [15], [5], [2],[11], [4],[10], [9],[12], [0], [3],[14], [8],[13], [6], [7], [1]],
                  [  [7], [2],[12], [5], [8], [4], [6],[11],[14], [9], [1],[15],[13], [3],[10], [0]],
                  [  [1],[13],[15], [0],[14], [8], [2],[11], [7], [4],[12],[10], [9], [3], [5], [6]],
                  )

serpentsboxesinverse = ([  [13], [3],[11], [0],[10], [6], [5],[12], [1],[14], [4], [7],[15], [9], [8], [2]],
                          [ [5], [8], [2],[14],[15], [6],[12], [3],[11], [4], [7], [9], [1],[13],[10], [0]],
                          [[12], [9],[15], [4],[11],[14], [1], [2], [0], [3], [6],[13], [5], [8],[10], [7]],
                          [ [0], [9],[10], [7],[11],[14], [6],[13], [3], [5],[12], [2], [4], [8],[15], [1]],
                          [ [5], [0], [8], [3],[10], [9], [7],[14], [2],[12],[11], [6], [4],[15],[13], [1]],
                          [ [8],[15], [2], [9], [4], [1],[13],[14],[11], [6], [5], [3], [7],[12],[10], [0]],
                          [[15],[10], [1],[13], [5], [3], [6], [0], [4], [9],[14], [7], [2],[12], [8],[11]],
                          [ [3], [0], [6],[13], [9],[14],[15], [8], [5],[12],[11], [7],[10], [1], [4], [2]],
                  )



IPTable = [
    0, 32, 64, 96, 1, 33, 65, 97, 2, 34, 66, 98, 3, 35, 67, 99,
    4, 36, 68, 100, 5, 37, 69, 101, 6, 38, 70, 102, 7, 39, 71, 103,
    8, 40, 72, 104, 9, 41, 73, 105, 10, 42, 74, 106, 11, 43, 75, 107,
    12, 44, 76, 108, 13, 45, 77, 109, 14, 46, 78, 110, 15, 47, 79, 111,
    16, 48, 80, 112, 17, 49, 81, 113, 18, 50, 82, 114, 19, 51, 83, 115,
    20, 52, 84, 116, 21, 53, 85, 117, 22, 54, 86, 118, 23, 55, 87, 119,
    24, 56, 88, 120, 25, 57, 89, 121, 26, 58, 90, 122, 27, 59, 91, 123,
    28, 60, 92, 124, 29, 61, 93, 125, 30, 62, 94, 126, 31, 63, 95, 127,
    ]
FPTable = [
    0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60,
    64, 68, 72, 76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124,
    1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57, 61,
    65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, 125,
    2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62,
    66, 70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110, 114, 118, 122, 126,
    3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55, 59, 63,
    67, 71, 75, 79, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 127,
 ]

##I had to borrow this from Dmytro Benedyk's version/the original Python ver
LTTable = [
    [16, 52, 56, 70, 83, 94, 105],
    [72, 114, 125],
    [2, 9, 15, 30, 76, 84, 126],
    [36, 90, 103],
    [20, 56, 60, 74, 87, 98, 109],
    [1, 76, 118],
    [2, 6, 13, 19, 34, 80, 88],
    [40, 94, 107],
    [24, 60, 64, 78, 91, 102, 113],
    [5, 80, 122],
    [6, 10, 17, 23, 38, 84, 92],
    [44, 98, 111],
    [28, 64, 68, 82, 95, 106, 117],
    [9, 84, 126],
    [10, 14, 21, 27, 42, 88, 96],
    [48, 102, 115],
    [32, 68, 72, 86, 99, 110, 121],
    [2, 13, 88],
    [14, 18, 25, 31, 46, 92, 100],
    [52, 106, 119],
    [36, 72, 76, 90, 103, 114, 125],
    [6, 17, 92],
    [18, 22, 29, 35, 50, 96, 104],
    [56, 110, 123],
    [1, 40, 76, 80, 94, 107, 118],
    [10, 21, 96],
    [22, 26, 33, 39, 54, 100, 108],
    [60, 114, 127],
    [5, 44, 80, 84, 98, 111, 122],
    [14, 25, 100],
    [26, 30, 37, 43, 58, 104, 112],
    [3, 118],
    [9, 48, 84, 88, 102, 115, 126],
    [18, 29, 104],
    [30, 34, 41, 47, 62, 108, 116],
    [7, 122],
    [2, 13, 52, 88, 92, 106, 119],
    [22, 33, 108],
    [34, 38, 45, 51, 66, 112, 120],
    [11, 126],
    [6, 17, 56, 92, 96, 110, 123],
    [26, 37, 112],
    [38, 42, 49, 55, 70, 116, 124],
    [2, 15, 76],
    [10, 21, 60, 96, 100, 114, 127],
    [30, 41, 116],
    [0, 42, 46, 53, 59, 74, 120],
    [6, 19, 80],
    [3, 14, 25, 100, 104, 118],
    [34, 45, 120],
    [4, 46, 50, 57, 63, 78, 124],
    [10, 23, 84],
    [7, 18, 29, 104, 108, 122],
    [38, 49, 124],
    [0, 8, 50, 54, 61, 67, 82],
    [14, 27, 88],
    [11, 22, 33, 108, 112, 126],
    [0, 42, 53],
    [4, 12, 54, 58, 65, 71, 86],
    [18, 31, 92],
    [2, 15, 26, 37, 76, 112, 116],
    [4, 46, 57],
    [8, 16, 58, 62, 69, 75, 90],
    [22, 35, 96],
    [6, 19, 30, 41, 80, 116, 120],
    [8, 50, 61],
    [12, 20, 62, 66, 73, 79, 94],
    [26, 39, 100],
    [10, 23, 34, 45, 84, 120, 124],
    [12, 54, 65],
    [16, 24, 66, 70, 77, 83, 98],
    [30, 43, 104],
    [0, 14, 27, 38, 49, 88, 124],
    [16, 58, 69],
    [20, 28, 70, 74, 81, 87, 102],
    [34, 47, 108],
    [0, 4, 18, 31, 42, 53, 92],
    [20, 62, 73],
    [24, 32, 74, 78, 85, 91, 106],
    [38, 51, 112],
    [4, 8, 22, 35, 46, 57, 96],
    [24, 66, 77],
    [28, 36, 78, 82, 89, 95, 110],
    [42, 55, 116],
    [8, 12, 26, 39, 50, 61, 100],
    [28, 70, 81],
    [32, 40, 82, 86, 93, 99, 114],
    [46, 59, 120],
    [12, 16, 30, 43, 54, 65, 104],
    [32, 74, 85],
    [36, 90, 103, 118],
    [50, 63, 124],
    [16, 20, 34, 47, 58, 69, 108],
    [36, 78, 89],
    [40, 94, 107, 122],
    [0, 54, 67],
    [20, 24, 38, 51, 62, 73, 112],
    [40, 82, 93],
    [44, 98, 111, 126],
    [4, 58, 71],
    [24, 28, 42, 55, 66, 77, 116],
    [44, 86, 97],
    [2, 48, 102, 115],
    [8, 62, 75],
    [28, 32, 46, 59, 70, 81, 120],
    [48, 90, 101],
    [6, 52, 106, 119],
    [12, 66, 79],
    [32, 36, 50, 63, 74, 85, 124],
    [52, 94, 105],
    [10, 56, 110, 123],
    [16, 70, 83],
    [0, 36, 40, 54, 67, 78, 89],
    [56, 98, 109],
    [14, 60, 114, 127],
    [20, 74, 87],
    [4, 40, 44, 58, 71, 82, 93],
    [60, 102, 113],
    [3, 18, 72, 114, 118, 125],
    [24, 78, 91],
    [8, 44, 48, 62, 75, 86, 97],
    [64, 106, 117],
    [1, 7, 22, 76, 118, 122],
    [28, 82, 95],
    [12, 48, 52, 66, 79, 90, 101],
    [68, 110, 121],
    [5, 11, 26, 80, 122, 126],
    [32, 86, 99],
    ]

LTTableInverse = [
    [53, 55, 72],
    [1, 5, 20, 90],
    [15, 102],
    [3, 31, 90],
    [57, 59, 76],
    [5, 9, 24, 94],
    [19, 106],
    [7, 35, 94],
    [61, 63, 80],
    [9, 13, 28, 98],
    [23, 110],
    [11, 39, 98],
    [65, 67, 84],
    [13, 17, 32, 102],
    [27, 114],
    [1, 3, 15, 20, 43, 102],
    [69, 71, 88],
    [17, 21, 36, 106],
    [1, 31, 118],
    [5, 7, 19, 24, 47, 106],
    [73, 75, 92],
    [21, 25, 40, 110],
    [5, 35, 122],
    [9, 11, 23, 28, 51, 110],
    [77, 79, 96],
    [25, 29, 44, 114],
    [9, 39, 126],
    [13, 15, 27, 32, 55, 114],
    [81, 83, 100],
    [1, 29, 33, 48, 118],
    [2, 13, 43],
    [1, 17, 19, 31, 36, 59, 118],
    [85, 87, 104],
    [5, 33, 37, 52, 122],
    [6, 17, 47],
    [5, 21, 23, 35, 40, 63, 122],
    [89, 91, 108],
    [9, 37, 41, 56, 126],
    [10, 21, 51],
    [9, 25, 27, 39, 44, 67, 126],
    [93, 95, 112],
    [2, 13, 41, 45, 60],
    [14, 25, 55],
    [2, 13, 29, 31, 43, 48, 71],
    [97, 99, 116],
    [6, 17, 45, 49, 64],
    [18, 29, 59],
    [6, 17, 33, 35, 47, 52, 75],
    [101, 103, 120],
    [10, 21, 49, 53, 68],
    [22, 33, 63],
    [10, 21, 37, 39, 51, 56, 79],
    [105, 107, 124],
    [14, 25, 53, 57, 72],
    [26, 37, 67],
    [14, 25, 41, 43, 55, 60, 83],
    [0, 109, 111],
    [18, 29, 57, 61, 76],
    [30, 41, 71],
    [18, 29, 45, 47, 59, 64, 87],
    [4, 113, 115],
    [22, 33, 61, 65, 80],
    [34, 45, 75],
    [22, 33, 49, 51, 63, 68, 91],
    [8, 117, 119],
    [26, 37, 65, 69, 84],
    [38, 49, 79],
    [26, 37, 53, 55, 67, 72, 95],
    [12, 121, 123],
    [30, 41, 69, 73, 88],
    [42, 53, 83],
    [30, 41, 57, 59, 71, 76, 99],
    [16, 125, 127],
    [34, 45, 73, 77, 92],
    [46, 57, 87],
    [34, 45, 61, 63, 75, 80, 103],
    [1, 3, 20],
    [38, 49, 77, 81, 96],
    [50, 61, 91],
    [38, 49, 65, 67, 79, 84, 107],
    [5, 7, 24],
    [42, 53, 81, 85, 100],
    [54, 65, 95],
    [42, 53, 69, 71, 83, 88, 111],
    [9, 11, 28],
    [46, 57, 85, 89, 104],
    [58, 69, 99],
    [46, 57, 73, 75, 87, 92, 115],
    [13, 15, 32],
    [50, 61, 89, 93, 108],
    [62, 73, 103],
    [50, 61, 77, 79, 91, 96, 119],
    [17, 19, 36],
    [54, 65, 93, 97, 112],
    [66, 77, 107],
    [54, 65, 81, 83, 95, 100, 123],
    [21, 23, 40],
    [58, 69, 97, 101, 116],
    [70, 81, 111],
    [58, 69, 85, 87, 99, 104, 127],
    [25, 27, 44],
    [62, 73, 101, 105, 120],
    [74, 85, 115],
    [3, 62, 73, 89, 91, 103, 108],
    [29, 31, 48],
    [66, 77, 105, 109, 124],
    [78, 89, 119],
    [7, 66, 77, 93, 95, 107, 112],
    [33, 35, 52],
    [0, 70, 81, 109, 113],
    [82, 93, 123],
    [11, 70, 81, 97, 99, 111, 116],
    [37, 39, 56],
    [4, 74, 85, 113, 117],
    [86, 97, 127],
    [15, 74, 85, 101, 103, 115, 120],
    [41, 43, 60],
    [8, 78, 89, 117, 121],
    [3, 90],
    [19, 78, 89, 105, 107, 119, 124],
    [45, 47, 64],
    [12, 82, 93, 121, 125],
    [7, 94],
    [0, 23, 82, 93, 109, 111, 123],
    [49, 51, 68],
    [1, 16, 86, 97, 125],
    [11, 98],
    [4, 27, 86, 97, 113, 115, 127],
]

def FuncTest(input,table):
    return applyperm(table, input)

def applyperm(table,input):
    data = ""
    for i in range(len(table)):
        data = data + input[table[i]]
    return data


LayerPInput=[]
def createinput():
    if len(ba) > 128:
        x= slice(0,128)
        LayerPInput=ba[x]
        del ba[0:128]
        return LayerPInput
    elif len(ba) == 128:
        x= slice(0,128)
        LayerPInput=ba[x]
        del ba[0:128]
        return LayerPInput

def bitslicesetup(input2, output):
    for i in range(0,32):
        tempSlice1 =input2[slice(i,i+1)]
        tempSlice2 =input2[slice(i+32,i+33)]
        tempSlice3 =input2[slice(i+64,i+65)]
        tempSlice4 =input2[slice(i+96,i+97)]
        LittleEndianByte= tempSlice1 +tempSlice2 + tempSlice3 + tempSlice4
        output.append(LittleEndianByte)
    del input2[0:128]

def slicesetup(input2, output):
    for i in range(0,32):
        LittleEndianByte =input2[slice(i*4,(i*4)+4)]       
        output.append(LittleEndianByte)
    del input2[0:128]



def changeendian(input,output, changetype): #0 for old changeendian, 4 for changeendianreverse
    output=bitarray()
    for i in range(0,16):
        tempslice=input[slice(128-((i+1)*8),128-((i)*8))]
        for i in range(0,1):
            tempslice2=tempslice[slice(0,4)]
            tempslice3=tempslice[slice(4,8)]
            if changetype == 0:
                tempslice2.reverse()
                tempslice3.reverse()                
            if changetype ==0:
                tempslice2+=tempslice3
                tempslice4=tempslice2
            if changetype ==4:
                tempslice3+=tempslice2
                tempslice4=tempslice3
        output=output+tempslice4
    if len(output) <128:
        lengthen8multinsertfront(output)
        while len(output) <128:
            output.reverse()
            output.append(0)
            output.fill()
            output.reverse()
    return output


def changeendianinput(input,output):
    output=bitarray()
    for i in range(0,16):
        tempslice=input[slice((i*8),(i+1)*8)]
        for i in range(0,1):
            tempslice2=tempslice[slice(0,8)]
            tempslice2.reverse()
        output += tempslice2
    if len(output) <128:
        lengthen8multinsertfront(output)
        while len(output) <128:
            output.reverse()
            output.append(0)
            output.fill()
            output.reverse()
    return output



###############################################################
###############################################################
###############################################################
####Key Generation


def keyschedule():
    keygen()
    basekeyworking = basekey.copy()
##########basekeyworking = truebasekey.copy()
    #print("Basekey: ",basekeyworking)
    #print("Basekey Hex",ba2hex(basekeyworking))
    #print("--------------------------------------------------")
    Oopsall1s256=bitarray(256)
    Oopsall1s256.setall(1)
    basekeyworkingInverse=basekeyworking^Oopsall1s256
    
    basekeyworking.bytereverse()
    basekeyworkingInverse.bytereverse()
    for i in range(0,8): #0,8
        tempSlice1 =basekeyworking[slice(0,32)]
        Key8wrds.append(tempSlice1)
        del basekeyworking[0:32]
    for i in range(0,8): #0,8
        tempSlice1Inverse =basekeyworkingInverse[slice(0,32)]
        Key8wrdsInverse.append(tempSlice1Inverse)
        del basekeyworkingInverse[0:32]
    
    prekey(Key8wrds)
    prekey(Key8wrdsInverse)
    del Key8wrds[0:8]
    del Key8wrdsInverse[0:8]  
    prekeynibblemaker(Key8wrds, Key8wrdsnibble)
    prekeynibblemaker(Key8wrdsInverse, Key8wrdsnibbleInverse)
    SBoxKeyTrue(Key8wrdsnibble, keysboxnibbleholder)
    SBoxKeyTrue(Key8wrdsnibbleInverse, keysboxnibbleholderInverse)
    keynibbleto32(keysboxnibbleholder, Key8wrdspostnibble, 33, 32)
    keynibbleto32(keysboxnibbleholderInverse, Key8wrdspostnibbleInverse, 33, 32)
    roundkeymaker(Key8wrdspostnibble, SubkeysKi)
    roundkeymaker(Key8wrdspostnibbleInverse,SubkeysKiInverse)



def keygen():
    for i in range(0,256):
        x = random.randint(0, 1)
        basekey.append(x)
    #print("Basekey: ",basekey)
def prekey(input):
    for i in range(8,140):
        prekeygenerator1=input[i-8]^input[i-5]^input[i-3]^input[i-1]    
        prekeygenerator2=ba2int(prekeygenerator1)^ba2int(fracgoldratio)^(i-8)
        temphold=int2ba(i-8)        
        if len(temphold) <32:
            lengthen8multinsertfront(temphold)
            while len(temphold) <32:
                temphold.reverse()
                temphold.append(0)
                temphold.fill()
                temphold.reverse()
        temphold.reverse()
        prekeygenerator2=prekeygenerator1^fracgoldratio^(temphold)
        prekeygenerator3=rshift(ba2int(prekeygenerator2),11)
        prekeygenerator3=int2ba(prekeygenerator3)
        extendlen(prekeygenerator3, input,32)

def prekeynibblemaker(input,output):
    for n in range(0,33): #33
        for i in range(0,32):
            tempSlice1 =input[0][0]
            tempSlice2 =input[1][0]
            tempSlice3 =input[2][0]
            tempSlice4 =input[3][0]
            del input[0][0], input[1][0], input[2][0], input[3][0]
            LittleEndianByte= str(tempSlice4) +str(tempSlice3) + str(tempSlice2) + str(tempSlice1)
            LittleEndianByte=int(LittleEndianByte,2)
            output.append(LittleEndianByte)
        del input[0:4]
def SBoxKeyTrue(input3,output):
    for i in range(0,4):
        for n in SBoxKeyList:
            for i in range(0,32):
                tempstorage1=[]
                Sbox(input3[0],tempstorage1,n)
                batemp1=int2ba(tempstorage1[0])    
                lengthen8multinsertfront4(batemp1)
                batemp1.reverse()
                output.append(batemp1)
                del input3[0]
            
    for i in range(0,32): ##last round
        tempstorage1=[]
        Sbox(input3[0],tempstorage1,3)  
        batemp1=int2ba(tempstorage1[0])
        lengthen8multinsertfront4(batemp1)
        batemp1.reverse()
        output.append(batemp1)
        del input3[0]

def keynibbleto32(input2,output,n1,n2): 
    for n in range(0,n1):
        tempword1=[]
        tempword2=[]
        tempword3=[]
        tempword4=[]
        for i in range(0,n2):            
            tempword1.append(input2[0][0])
            tempword2.append(input2[0][1])
            tempword3.append(input2[0][2])
            tempword4.append(input2[0][3])
            del input2[0]
        string1 = [str(int) for int in tempword1]
        string11 = "".join(string1)
        string2 = [str(int) for int in tempword2]
        string22 = "".join(string2)
        string3 = [str(int) for int in tempword3]
        string33 = "".join(string3)
        string4 = [str(int) for int in tempword4]
        string44 = "".join(string4)
        output.append(string11)
        output.append(string22)
        output.append(string33)
        output.append(string44)
        del string1, string2, string3, string4, string11, string22, string33, string44, tempword1, tempword2, tempword3, tempword4
def roundkeymaker(input,input2): 
    for i in range(0,33): 
        temphold=input[0]+input[1]+input[2]+input[3]
        prekeygenerator3=int(temphold,2)
        prekeygenerator3=int2ba(prekeygenerator3)
        extend128P(prekeygenerator3, input2,IPTable)
        del input[0:4]
###############################################################
###############################################################
###############################################################
###Misc Functions that get used a lot
        
def ROR4(Input, RotationAmount):
    return (Input >> RotationAmount)|(Input << (4 - RotationAmount)) & 0xFFFFFFFF

def lshift(x, n):
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

def rshift(x, n):
    return (x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)

def Sbox(inputnibble, outputnibble, Si):
    czz= inputnibble
    cff= serpentsboxes[Si][czz]
    cff=cff[0]
    outputnibble.append(cff)

def lengthen8multinsertfront(Input):
    Input.reverse()
    Input.fill()
    Input.reverse()
def lengthen8multinsertfront4(Input):
    Input.reverse()
    if len(Input)==1:
       Input.append(0)
       Input.append(0)
       Input.append(0)
    elif len(Input)== 2:
        Input.append(0)
        Input.append(0)
    elif len(Input)== 3:
        Input.append(0)

    Input.reverse()

def SboxBigFunc(inputnibble, outputnibble, Si):
    for n in range(0,len(inputnibble)):
        czz= inputnibble[n]
        czz.reverse()
        czz=ba2int(czz)
        cff= serpentsboxes[Si][czz]
        cff=int2ba(cff[0])
        lengthen8multinsertfront4(cff)
        cff.reverse()
        outputnibble.append(cff)






def extend128P(input2,output,choice): #IPTable for IP, FPTable for FP
    testing=bitarray()
    if len(input2) <128:
        lengthen8multinsertfront(input2)
        while len(input2) <128:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    for i in range(len(input2)):
        testing += int2ba(input2[choice[i]])  
    if len(testing) <128:
        lengthen8multinsertfront(testing)
        while len(testing) <128:
            testing.reverse()
            testing.append(0)
            testing.fill()
            testing.reverse()
    output.append(testing)

        
    
       


###############################################################
###############################################################
############################################################### 


def SerpentRounds3(Input): 
    BIntermediate128=bitarray()
    BIntermediate32Word3=[]
    for i in range(0,31): 
        BIntermediateXORed= Input^SubkeysKi[i]
        slicesetup(BIntermediateXORed, BIntermediateBitSliced)
        SboxBigFunc(BIntermediateBitSliced, BIntermediateBitSlicedSBoxed, (i % 8))
        BIntermediate32Word=''
        for i in range(0, len(BIntermediateBitSlicedSBoxed),2):
            tempword1=[]
            tempword2=[]      
            temp11str=str(BIntermediateBitSlicedSBoxed[0])
            temp11str=temp11str[10:-2]   
            temp22str=str(BIntermediateBitSlicedSBoxed[1])
            temp22str=temp22str[10:-2]
            temphold=temp11str+temp22str
            BIntermediate32Word=BIntermediate32Word+temphold
            del BIntermediateBitSlicedSBoxed[0:2]
        BIntermediate32Word=LinTransform(BIntermediate32Word)
        BIntermediate32Word=int(BIntermediate32Word,2)   
        BIntermediate32Word=int2ba(BIntermediate32Word)
        if len(BIntermediate32Word) <128:
            lengthen8multinsertfront(BIntermediate32Word)
            while len(BIntermediate32Word) <128:
                BIntermediate32Word.reverse()
                BIntermediate32Word.append(0)
                BIntermediate32Word.fill()
                BIntermediate32Word.reverse()
        del Input
        Input = BIntermediate32Word.copy()
        del BIntermediate32Word[:], BIntermediateBitSlicedSBoxed[:],BIntermediateBitSliced[:],BIntermediateXORed[:]


    BIntermediateXORed= Input^SubkeysKi[31]
    slicesetup(BIntermediateXORed, BIntermediateBitSliced)
    SboxBigFunc(BIntermediateBitSliced, BIntermediateBitSlicedSBoxed, (31 % 8))
    BIntermediate32Word=''
    BIntermediate32Word2=[]
    for i in range(0, len(BIntermediateBitSlicedSBoxed),2):
        tempword1=[]
        tempword2=[]      
        temp11str=str(BIntermediateBitSlicedSBoxed[0])
        temp11str=temp11str[10:-2]   
        temp22str=str(BIntermediateBitSlicedSBoxed[1])
        temp22str=temp22str[10:-2]
        temphold=temp11str+temp22str
        BIntermediate32Word=BIntermediate32Word+temphold
        del BIntermediateBitSlicedSBoxed[0:2]
    BIntermediate32Word=int(BIntermediate32Word,2)
    BIntermediate32Word=int2ba(BIntermediate32Word)
    extendlen(BIntermediate32Word, BIntermediate32Word2,128)
    del Input
    Input=BIntermediate32Word2[0]^SubkeysKi[32]
    return Input


    





def LinTransform(input):
    """Apply the table-based version of the linear transformation to the
    128-bit string 'input' and return a 128-bit string as the result."""
    ##I had to borrow this from Dmytro Benedyk's version/the original Python ver

  
    result = ""
    for i in range(len(LTTable)):
        outputBit = "0"
        for j in LTTable[i]:
            outputBit = int(outputBit)^int(input[j])
        result = result + str(outputBit)
    return result



FinalWord3=''
FinalWord0=[]
FinalWord3inverse=''
FinalWord0inverse=[]


def SerpentRunWXor():
    FinalWord=[]
    FinalWordInverse=[]
    LayerPInput=createinput()
    Oopsall1s=bitarray(128)
    Oopsall1s.setall(1)
    LayerPInputInverse=LayerPInput^Oopsall1s
    
    LayerPInput2=''
    LayerPInput5=[]
    LayerPInput2inverse=''
    LayerPInput5inverse=[]
    
    LayerPInput3=changeendianinput(LayerPInput,LayerPInput2)
    LayerPInput3inverse=changeendianinput(LayerPInputInverse,LayerPInput2inverse)
    LayerPInput3=str(LayerPInput3)
    LayerPInput3inverse=str(LayerPInput3inverse)

    
    LayerPInput3=LayerPInput3[10:-2]
    LayerPInput3inverse=LayerPInput3inverse[10:-2]  
    LayerPInput4 = FuncTest(LayerPInput3,IPTable)
    LayerPInput4inverse=FuncTest(LayerPInput3inverse,IPTable)

    LayerPInput4=int2ba(int(LayerPInput4,2))
    LayerPInput4inverse=int2ba(int(LayerPInput4inverse,2))
    extendlen(LayerPInput4, LayerPInput5,128)
    extendlen(LayerPInput4inverse, LayerPInput5inverse,128)
    
    LayerPInput=SerpentRounds3(LayerPInput5[0])
    LayerPInputInverse=SerpentRounds3(LayerPInput5inverse[0])
    LayerPInput=str(LayerPInput)
    LayerPInputInverse=str(LayerPInputInverse)
    
    LayerPInput=LayerPInput[10:-2]
    LayerPInputInverse=LayerPInputInverse[10:-2]
    FinalWord = FuncTest(LayerPInput,FPTable)
    FinalWordInverse=FuncTest(LayerPInputInverse,FPTable)

    
    FinalWord=int2ba(int(FinalWord,2))
    FinalWordInverse=int2ba(int(FinalWordInverse,2))
    extendlen(FinalWord, FinalWord0,128)
    extendlen(FinalWordInverse,FinalWord0inverse,128)
    
    
    FinalWord2=changeendian(FinalWord0[0],FinalWordEndian, 4)
    FinalWord2inverse=changeendian(FinalWord0inverse[0],FinalWordEndianInverse, 4)
    FinalWord3=changeendian(FinalWord2,FinalWordEndian2, 0)
    FinalWord3Inverse=changeendian(FinalWord2inverse,FinalWordEndian2Inverse, 0)

    FinalWordFull=''
    FinalWordFullInverse=''
    FinalWordFull=str(FinalWord3)
    FinalWordFullInverse=str(FinalWord3Inverse)
        
    FinalWordFull=FinalWordFull[10:-2]
    FinalWordFullInverse=FinalWordFullInverse[10:-2]
    FinalWordFullHex=hex(int(FinalWordFull,2))
    FinalWordFullHexInverse=hex(int(FinalWordFullInverse,2))
    #print("FinalWordFull: ",FinalWordFull)
    
    #print("FinalWordFullHex: ",FinalWordFullHex)
    #print("--------------------------------------------------")
    print(FinalWordFull,file=exampleoutput, end = "")
    #SerpentDecrypt(FinalWord3)
    return 

WordEndian2=''


def SerpentDecrypt(Input):
    print("In progress")
    Word3=[]
    Word0=changeendian(Input,WordEndian, 0)
    Word1=changeendian(Word0,WordEndian2, 4)
    Word2 = FuncTest(Word1,IPTable)
    Word2=int2ba(int(Word2,2))   
    extendlen(Word2, Word3,128)
    LayerPInput=SerpentRounds3(LayerPInput5[0])  #this is like... def wrong lol

#####I need to clean up the code
#####I need to add a decrypt mode
   
filetoopen='exampletext.txt'
#filetoopen=truefilename
ba = bitarray()
exampleoutput=open('exampleoutput.txt','w')
#f = open(filetoopen, 'rb')
#ba.fromfile(f)


#for i in range(0,128): #442128 for big tests
#        x = random.randint(0, 1)
#        ba.append(x)

ba=bitarray('100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000100110001100001000110000100010011011000001001001101100010001100100011110001101011000101010100110110111101010111100000011001000001001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000')
#print("Length of File in bits: ",len(ba))
ba.reverse()
ba.fill()
ba.reverse()

#print("Length of File in bits after fill: ",len(ba))
#print("File in bits: ",ba)
#print("File Hex",ba2hex(ba))
#print("--------------------------------------------------")







#key 1001100011000010001100001000100110110000010010011011000100011001000111100011010110001010101001101101111010101111000000110010000010011000110000100011000010001001101100000100100110110001000110010001111000110101100010101010011011011110101011110000001100100000












keyschedule()


while len(ba) > 128:
    SerpentRunWXor()
    #print("BA Length: ",len(ba))

if len(ba) == 128:
    SerpentRunWXor()
    #print("BA Length: ",len(ba))
    
if len(ba) < 128:
    if len(ba) > 0:
        lengthen8multinsertfront(ba)
        while len(ba) <128:
            ba.reverse()
            ba.append(0)
            ba.fill()
            ba.reverse()
        SerpentRunWXor()



print("Execution Complete")
print("--- %s seconds ---" % (time.time() - start_time))
exampleoutput.close()



