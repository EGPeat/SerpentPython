import bitarray
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from bitarray.util import zeros
from bitarray.util import serialize
from bitarray.util import ba2hex
from bitarray.util import make_endian


import random
import numpy as np
import math
import galois

import time
start_time = time.time()


LayerPInput=[]
Player=[]
basekey=bitarray()
basekeyworking=[]
Key8wrds=[]
prekeyschedule=[]
Key8wrdsnibble=[]
Key8wrdsnibblesboxes=[]
keyschedulesboxes=[]
IP=[]
EP=[]
roundkeys=[]
SBoxKeyList=[3,2,1,0,7,6,5,4]
PlayerIPed=[]
keysboxnibbleholder=[]
Playerinputnibble=[]
Playeroutputnibble=[]
Key8wrdspostnibble=[]
tempword1=[]
tempword2=[]
tempword3=[]
tempword4=[]
SubkeysKi=[]
BIntermediateXORed=[]
BIntermediateBitSliced=[]
BIntermediateBitSlicedSBoxed=[]
BIntermediate32Word=[]
BIntermediate32LinMixed=[]
LayerPInputEndian=''
BIntermediate32WordBA=[]
FinalWordEndian=''
FinalWordEndian2=''
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

    
def IPFunctionInput(Input,Output):
    modifytoba=''
    modifytoba=IPFunction(Input, modifytoba)
    modifytoba2=int(modifytoba,2)
    modifytoba2=int2ba(modifytoba2)
    if len(modifytoba2) <128:
        lengthen8multinsertfront(modifytoba2)
        while len(modifytoba2) <128:
            modifytoba2.reverse()
            modifytoba2.append(0)
            modifytoba2.fill()
            modifytoba2.reverse()
    Output=modifytoba2
    return Output 



def IPFuncTest(input):
    return applyperm(IPTable, input)
def FPFuncTest(input):
    return applyperm(FPTable, input)

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



def changeendian(input,output):
    output=''
    for i in range(0,16):
        tempslice=input[slice(128-((i+1)*8),128-((i)*8))]
        for i in range(0,1):
            tempslice2=tempslice[slice(0,4)]
            tempslice3=tempslice[slice(4,8)]
            tempslice2.reverse()
            tempslice3.reverse()
            tempslice2=str(tempslice2)
            tempslice3=str(tempslice3)
            tempslice2=tempslice2.replace("bitarray('",'')
            tempslice2=tempslice2.replace("')",'')
            tempslice3=tempslice3.replace("bitarray('",'')
            tempslice3=tempslice3.replace("')",'')
            tempslice4=tempslice2+tempslice3
        output=output+tempslice4
    output=int(output,2)
    output=int2ba(output)
    if len(output) <128:
        lengthen8multinsertfront(output)
        while len(output) <128:
            output.reverse()
            output.append(0)
            output.fill()
            output.reverse()
    return output

def changeendianinput(input,output):
    output=''
    for i in range(0,16):
        tempslice=input[slice((i*8),(i+1)*8)]
        for i in range(0,1):
            tempslice2=tempslice[slice(0,8)]
            tempslice2.reverse()
            tempslice2=str(tempslice2)
            tempslice2=tempslice2.replace("bitarray('",'')
            tempslice2=tempslice2.replace("')",'')
            tempslice4=tempslice2
        output=output+tempslice4
    output=int(output,2)
    output=int2ba(output)
    if len(output) <128:
        lengthen8multinsertfront(output)
        while len(output) <128:
            output.reverse()
            output.append(0)
            output.fill()
            output.reverse()
    return output


def changeendiannoreverse(input,output):
    output=''
    for i in range(0,16):
        tempslice=input[slice(128-((i+1)*8),128-((i)*8))]
        for i in range(0,1):
            tempslice2=tempslice[slice(0,4)]
            tempslice3=tempslice[slice(4,8)]
            tempslice2=str(tempslice2)
            tempslice3=str(tempslice3)
            tempslice2=tempslice2.replace("bitarray('",'')
            tempslice2=tempslice2.replace("')",'')
            tempslice3=tempslice3.replace("bitarray('",'')
            tempslice3=tempslice3.replace("')",'')
            tempslice4=tempslice3+tempslice2
        output=output+tempslice4
    output=int(output,2)
    output=int2ba(output)
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
    #basekey=bitarray('0100111101001111011101101011110100100100011011001100101101101000000000000111111000001101011010000111001101100000001100111100011101110111110100000010011001101001010101011101101011110111100011100011110110011110000111001111101010110100000110001000111110010100')
    print("Basekey: ",basekey)
    print("Basekey Hex",ba2hex(basekey))
    print("--------------------------------------------------")
    basekeyworking = basekey.copy()
    basekeyworking.bytereverse()
    for i in range(0,8): #0,8
        tempSlice1 =basekeyworking[slice(0,32)]
        Key8wrds.append(tempSlice1)
        del basekeyworking[0:32]
    prekey()
    del Key8wrds[0:8]   
    prekeynibblemaker()   
    SBoxKeyTrue(Key8wrdsnibble)
    keynibbleto32(keysboxnibbleholder, Key8wrdspostnibble, 33, 32)
    roundkeymaker()




def keygen():
    for i in range(0,256):
        x = random.randint(0, 1)
        basekey.append(x)
    #print("Basekey: ",basekey)
def prekey():
    for i in range(8,140):
        prekeygenerator1=Key8wrds[i-8]^Key8wrds[i-5]^Key8wrds[i-3]^Key8wrds[i-1]    
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
        extend32(prekeygenerator3, Key8wrds)

def prekeynibblemaker():
    for n in range(0,33): #33
        for i in range(0,32):
            tempSlice1 =Key8wrds[0][0]
            tempSlice2 =Key8wrds[1][0]
            tempSlice3 =Key8wrds[2][0]
            tempSlice4 =Key8wrds[3][0]
            del Key8wrds[0][0], Key8wrds[1][0], Key8wrds[2][0], Key8wrds[3][0]
            LittleEndianByte= str(tempSlice4) +str(tempSlice3) + str(tempSlice2) + str(tempSlice1)
            LittleEndianByte=int(LittleEndianByte,2)
            Key8wrdsnibble.append(LittleEndianByte)
        del Key8wrds[0:4]
def SBoxKeyTrue(input3):
    for i in range(0,4):
        for n in SBoxKeyList:
            for i in range(0,32):
                tempstorage1=[]
                Sbox(input3[0],tempstorage1,n)
                batemp1=int2ba(tempstorage1[0])
                lengthen8multinsertfront4(batemp1)
                batemp1.reverse()
                keysboxnibbleholder.append(batemp1)
                del input3[0]
            
    for i in range(0,32): ##last round
        tempstorage1=[]
        Sbox(input3[0],tempstorage1,3)
        batemp1=int2ba(tempstorage1[0])
        lengthen8multinsertfront4(batemp1)
        batemp1.reverse()
        keysboxnibbleholder.append(batemp1)
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
def roundkeymaker(): 
    for i in range(0,33): 
        temphold=Key8wrdspostnibble[0]+Key8wrdspostnibble[1]+Key8wrdspostnibble[2]+Key8wrdspostnibble[3]
        prekeygenerator3=int(temphold,2)
        prekeygenerator3=int2ba(prekeygenerator3)
        extend128IP(prekeygenerator3, SubkeysKi)
        del Key8wrdspostnibble[0:4]
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
        cff=cff[0]
        cff=int2ba(cff)
        lengthen8multinsertfront4(cff)
        cff.reverse()
        outputnibble.append(cff)



def extend32(input2, output):
    if len(input2) <32:
        lengthen8multinsertfront(input2)
        while len(input2) <32:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    output.append(input2)
def extend128(input2, output):
    if len(input2) <128:
        lengthen8multinsertfront(input2)
        while len(input2) <128:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    output.append(input2)

def extend128IP(input2, output):
    testing=''
    if len(input2) <128:
        lengthen8multinsertfront(input2)
        while len(input2) <128:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    for i in range(len(input2)):
        testing = testing + str(input2[IPTable[i]])
    testing=int(testing,2)
    testing=int2ba(testing)
    if len(testing) <128:
        lengthen8multinsertfront(testing)
        while len(testing) <128:
            testing.reverse()
            testing.append(0)
            testing.fill()
            testing.reverse()
    output.append(testing)
def extend128FP(input2, output):
    testing=''
    if len(input2) <128:
        lengthen8multinsertfront(input2)
        while len(input2) <128:
            input2.reverse()
            input2.append(0)
            input2.fill()
            input2.reverse()
    for i in range(len(input2)):
        testing = testing + str(input2[FPTable[i]])
    testing=int(testing,2)
    testing=int2ba(testing)
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

    for i in range(0,31): 
        BIntermediateXORed= Input^SubkeysKi[i]
        slicesetup(BIntermediateXORed, BIntermediateBitSliced)
        SboxBigFunc(BIntermediateBitSliced, BIntermediateBitSlicedSBoxed, (i % 8))
        BIntermediate32Word=''
        for i in range(0, len(BIntermediateBitSlicedSBoxed),2):
            #print("len(BIntermediateBitSlicedSBoxed)",len(BIntermediateBitSlicedSBoxed))
            tempword1=[]
            tempword2=[]      
            temp11str=BIntermediateBitSlicedSBoxed[0].to01()
            temp22str=BIntermediateBitSlicedSBoxed[1].to01()        
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
    for i in range(0, len(BIntermediateBitSlicedSBoxed),2):
        tempword1=[]
        tempword2=[]      
        temp11str=BIntermediateBitSlicedSBoxed[0].to01()
        temp22str=BIntermediateBitSlicedSBoxed[1].to01()        
        temphold=temp11str+temp22str
        BIntermediate32Word=BIntermediate32Word+temphold
        del BIntermediateBitSlicedSBoxed[0:2]
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
    Input=BIntermediate32Word^SubkeysKi[32]
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


def SerpentRun():
    FinalWord=[]
    LayerPInput=createinput()
    LayerPInput2=''
    LayerPInput3=changeendianinput(LayerPInput,LayerPInput2)
    LayerPInput3=str(LayerPInput3)
    LayerPInput3=LayerPInput3.replace("bitarray('",'')
    LayerPInput3=LayerPInput3.replace("')",'')
    LayerPInput4 = IPFuncTest(LayerPInput3)
    LayerPInput4=int(LayerPInput4,2)
    LayerPInput4=int2ba(LayerPInput4)
    if len(LayerPInput4) <128:
        lengthen8multinsertfront(LayerPInput4)
        while len(LayerPInput4) <128:
            LayerPInput4.reverse()
            LayerPInput4.append(0)
            LayerPInput4.fill()
            LayerPInput4.reverse()
    LayerPInput=SerpentRounds3(LayerPInput4)
    LayerPInput=str(LayerPInput)
    LayerPInput=LayerPInput.replace("bitarray('",'')
    LayerPInput=LayerPInput.replace("')",'')
    FinalWord = FPFuncTest(LayerPInput)
    FinalWord=int(FinalWord,2)
    FinalWord=int2ba(FinalWord)
    if len(FinalWord) <128:
        lengthen8multinsertfront(FinalWord)
        while len(FinalWord) <128:
            FinalWord.reverse()
            FinalWord.append(0)
            FinalWord.fill()
            FinalWord.reverse()        
    FinalWord2=changeendiannoreverse(FinalWord,FinalWordEndian)
    FinalWord3=changeendian(FinalWord2,FinalWordEndian2)
    FinalWordFull=''
    FinalWordFull=str(FinalWord3)
    FinalWordFull=FinalWordFull.replace("bitarray('",'')
    FinalWordFull=FinalWordFull.replace("')",'')
    FinalWordFullHex=hex(int(FinalWordFull,2))
    print("FinalWordFull: ",FinalWordFull)
    print("FinalWordFullHex: ",FinalWordFullHex)
    print("--------------------------------------------------")
    print(FinalWordFull,file=exampleoutput, end = "")
    return 

    

#####I need to clean up the code
#####I need to add a decrypt mode
   
    
ba = bitarray()
exampleoutput=open('exampleoutput.txt','w')
#f = open('exampletext.txt', 'rb')
#ba.fromfile(f)


for i in range(0,422128):
        x = random.randint(0, 1)
        ba.append(x)
#ba=bitarray('10100100101110001111101011001110111010111101001110000111010110101010100001001100001010011011001111011100010011111100101001110000')

print("Length of File in bits: ",len(ba))
ba.reverse()
ba.fill()
ba.reverse()

print("Length of File in bits after fill: ",len(ba))
print("File in bits: ",ba)
print("File Hex",ba2hex(ba))
print("--------------------------------------------------")


keyschedule()


while len(ba) > 128:
    SerpentRun()
    print("BA Length: ",len(ba))

if len(ba) == 128:
    SerpentRun()
    print("BA Length: ",len(ba))
    
if len(ba) < 128:
    if len(ba) > 0:
        lengthen8multinsertfront(ba)
        while len(ba) <128:
            ba.reverse()
            ba.append(0)
            ba.fill()
            ba.reverse()
        SerpentRun()


#SerpentDecrypt()
print("Execution Complete")
print("--- %s seconds ---" % (time.time() - start_time))
exampleoutput.close()



