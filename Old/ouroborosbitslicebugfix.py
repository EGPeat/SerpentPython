import bitarray
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from bitarray.util import zeros
from bitarray.util import serialize
from bitarray.util import ba2hex
from bitarray.util import make_endian

#from bitarray import endian

#from bitarray import to01
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
###Serpent seems to be written to be both executed in Bitslice mode as well as 
###in standard mode. This makes... it kinda confusing to figure out what to do
###and can lead to potential error. I will need to get that fixed.
###could also mean we have several ways to run it.
fracgoldratio=2654435769
serpentsboxes = ([   [3], [8],[15], [1],[10], [6], [5],[11],[14],[13], [4], [2], [7], [0], [9],[12]],
                  [ [15],[12], [2], [7], [9], [0], [5],[10], [1],[11],[14], [8], [6],[13], [3], [4]],
                  [  [8], [6], [7], [9], [3],[12],[10],[15],[13], [1],[14], [4], [0],[11], [5], [2]],
                  [  [0],[15],[11], [8],[12], [9], [6], [3],[13], [1], [2], [4],[10], [7], [5],[14]],
                  [  [1],[15], [8], [3],[12], [0],[11], [6], [2], [5], [4],[10], [9],[14], [7],[13]],
                  [ [15], [5], [2],[11], [4],[10], [9],[12], [0], [3],[14], [8],[13], [6], [7], [1]],
                  [  [7], [2],[12], [5], [8], [4], [6],[11],[14], [9], [1],[15],[13], [3],[10], [0]],
                  [  [1],[13],[15], [0],[14], [6], [2],[11], [7], [4],[12],[10], [9], [3], [5], [6]],
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

###applysboxes
    #change variable names n shit
    #make sure stuff outputs right
###i have 0 clue if this works, it'll take a ton of effort to check
def IPFunction(Input, Output):
    for i in range(len(Input)):
        Output = Output + str(Input[IPTable[i]])
    return Output

def FPFunction(Input, Output):
    for i in range(len(Input)):
        Output = Output + str(Input[FPTable[i]])       
    return Output
    
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
    

LayerPInput=[]
def createinput():
    if len(ba) > 128:
        x= slice(0,128)
        LayerPInput=ba[x]
        #LayerPInput.append(ba[x])
        del ba[0:128]
        return LayerPInput
    elif len(ba) == 128:
        x= slice(0,128)
        LayerPInput=ba[x]
        #LayerPInput.append(ba[x])
        del ba[0:128]
        return LayerPInput

def bitslicesetup(input2, output):
    for i in range(0,32):
        tempSlice1 =input2[slice(i,i+1)]
        tempSlice2 =input2[slice(i+32,i+33)]
        tempSlice3 =input2[slice(i+64,i+65)]
        tempSlice4 =input2[slice(i+96,i+97)]
        LittleEndianByte= tempSlice1 +tempSlice2 + tempSlice3 + tempSlice4
        #print("LittleEndianByte: ",LittleEndianByte)
        output.append(LittleEndianByte)
    #print("LayerPInput: ",LayerPInput)
    del input2[0:128]


    
###############################################################
###############################################################
###############################################################
####Key Generation 
def keyschedule():
    #keygen()
    basekey=bitarray('1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
    print("Basekey: ",basekey)
    basekeyworking = basekey.copy()
    basekeyworking.bytereverse()
    for i in range(0,8):
        tempSlice1 =basekeyworking[slice(0,32)]
        #print(tempSlice1)
        Key8wrds.append(tempSlice1)
        #print(type(Key8wrds[i]))
        del basekeyworking[0:32]
    #print(Key8wrds)
    prekey()
    
    del Key8wrds[0:8]
    prekeynibblemaker()
    #print(Key8wrdsnibble)
    #print(len(Key8wrdsnibble))
    SBoxKeyTrue(Key8wrdsnibble)
    keynibbleto32(keysboxnibbleholder, Key8wrdspostnibble, 33, 32)
    roundkeymaker()



def keygen():
    for i in range(0,256):
        x = random.randint(0, 1)
        basekey.append(x)
    print("Basekey: ",basekey)
def prekey():
    for i in range(8,140):
        prekeygenerator1=Key8wrds[i-8]^Key8wrds[i-5]^Key8wrds[i-3]^Key8wrds[i-1]
        prekeygenerator2=ba2int(prekeygenerator1)^fracgoldratio^i
        #print("PrekeyCheck:",prekeygenerator3)
        prekeygenerator3=lshift(prekeygenerator2,11)
        #print("PrekeyCheck:",prekeygenerator3)
        prekeygenerator3=int2ba(prekeygenerator3)
        extend32(prekeygenerator3, Key8wrds)

def prekeynibblemaker():
    for n in range(0,33):
        #print("Large Round: ",n)
        for i in range(0,32):
            #print("Small Round:",i)
            tempSlice1 =Key8wrds[0].pop()
            tempSlice2 =Key8wrds[1].pop()
            tempSlice3 =Key8wrds[2].pop()
            tempSlice4 =Key8wrds[3].pop()
            LittleEndianByte= tempSlice1 +tempSlice2 + tempSlice3 + tempSlice4
            #print("LittleEndianByte: ",LittleEndianByte)
            Key8wrdsnibble.append(LittleEndianByte)
        #print("LayerPInput: ",LayerPInput)
        del Key8wrds[0:4]
def SBoxKeyTrue(input3):
    for i in range(0,4):
        for n in SBoxKeyList:
            for i in range(0,32):
                tempstorage1=[]
                Sbox(input3[0],tempstorage1,n)
                batemp1=int2ba(tempstorage1[0])
                lengthen8multinsertfront4(batemp1)
                keysboxnibbleholder.append(batemp1)
                del input3[0]
    for i in range(0,32): ##last round
        tempstorage1=[]
        Sbox(input3[0],tempstorage1,n)
        batemp1=int2ba(tempstorage1[0])
        lengthen8multinsertfront4(batemp1)
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
 ####good spot to convert string to BA through Int if need be
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

def roundkeymaker(): #input is keyscheduleboxes, output roundkeys
    for i in range(0,33): ###setup range to be 33 or 2
        temphold=Key8wrdspostnibble[0]+Key8wrdspostnibble[1]+Key8wrdspostnibble[2]+Key8wrdspostnibble[3]
        prekeygenerator3=int(temphold,2)
        prekeygenerator3=int2ba(prekeygenerator3)
        #extend128IP(prekeygenerator3, SubkeysKi)
        extend128(prekeygenerator3, SubkeysKi)
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
    #print(czz)
    #print(Si)
    cff= serpentsboxes[Si][czz]
    cff=cff[0]
    ###or have  cff= SBoxDecimalTable[Si][czz]
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
        czz=ba2int(czz)
        cff= serpentsboxes[Si][czz]
        cff=cff[0]
        cff=int2ba(cff)
        lengthen8multinsertfront4(cff)
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
    #print("Input2",ba2int(input2))
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
    #print("Input2IPed",ba2int(testing))
    output.append(testing)

###############################################################
###############################################################
############################################################### 


        


def SerpentRounds2(Input): #this one works with RIRoundFunc as it is rn
    BIntermediate=Input
    for i in range(0,8):
        RIRoundFunc(BIntermediate, i)
    for i in range(0,8):
        RIRoundFunc(BIntermediate, i+8)
    for i in range(0,8):
        RIRoundFunc(BIntermediate, i+16)
    for i in range(0,7):
       RIRoundFunc(Input, i)
    Input=LastRoundFunc(Input)
    return Input
    #maybe i need to use return? or append, idk. Return seems more likely.


BIntermediate32WordBA=[]

def RIRoundFunc(Input, Round): #add output section to RIRoundFunc
    BIntermediateXORed= Input^SubkeysKi[Round]
    bitslicesetup(BIntermediateXORed, BIntermediateBitSliced)
    SboxBigFunc(BIntermediateBitSliced, BIntermediateBitSlicedSBoxed, (Round % 8))
    keynibbleto32(BIntermediateBitSlicedSBoxed,BIntermediate32Word,1,32)
    for n in range(0,4):
        temp23=int(BIntermediate32Word[n],2)
        #temp33=int2ba(temp23)
        #lengthen8multinsertfront(temp33)
        BIntermediate32WordBA.append(temp23) #change to 33 if want BA
    LinearTransformationSerp(BIntermediate32WordBA,BIntermediate32LinMixed)
    del Input#, BIntermediate32WordBA[:]
    Input=BIntermediate32LinMixed[0]
    return Input
    #have the output actually go to the input variable and replace it

#### setup last round func
def LastRoundFunc(Input):
    BIntermediateXORed= Input^SubkeysKi[31]
    bitslicesetup(BIntermediateXORed, BIntermediateBitSliced)
    SboxBigFunc(BIntermediateBitSliced, BIntermediateBitSlicedSBoxed, 7)
    keynibbleto32(BIntermediateBitSlicedSBoxed,BIntermediate32Word,1,32)
    for n in range(0,4):
        temp23=int(BIntermediate32Word[n],2)
        temp33=int2ba(temp23)
        lengthen8multinsertfront(temp33)
        BIntermediate32WordBA.append(temp33) #change to 33 if want BA
    temp00str=BIntermediate32WordBA[0].to01()
    temp11str=BIntermediate32WordBA[1].to01()
    temp22str=BIntermediate32WordBA[2].to01()
    temp33str=BIntermediate32WordBA[3].to01()
    temphold=temp00str+temp11str+temp22str+temp33str
    tempoutputyes=int(temphold,2)
    tempoutputyes=int2ba(tempoutputyes)
    tempoutputyesyes=[]
    extend128(tempoutputyes,tempoutputyesyes)
    del Input, BIntermediate32WordBA[:]
    Input=tempoutputyesyes[0]^SubkeysKi[32]
    print(Input)
    return Input


####then make the entire whole thing loop lol                
def LinearTransformationSerp(input2,output):
    temp00=[]
    temp11=[]
    temp22=[]
    temp33=[]
    tempoutputyesyes=[]
    temp0=lshift(input2[0], 13)
    temp2=lshift(input2[2],3)
    temp1=input2[1]^temp0^temp2
    temp3=input2[3]^temp2^(temp0<<2)
    temp1=lshift(temp1,1)
    temp3=lshift(temp3,7)
    temp0=temp0^temp1^temp3
    temp2=temp2^temp3^(temp1<<7)
    temp0=lshift(temp0,5)
    temp2=lshift(temp2,22)
    temp0=int2ba(temp0)
    temp1=int2ba(temp1)
    temp2=int2ba(temp2)
    temp3=int2ba(temp3)
    extend32(temp0, temp00)
    extend32(temp1, temp11)
    extend32(temp2, temp22)
    extend32(temp3, temp33)
    del input2[0:4]
    temp00str=temp00[0].to01()
    temp11str=temp11[0].to01()
    temp22str=temp22[0].to01()
    temp33str=temp33[0].to01()
    temphold=temp00str+temp11str+temp22str+temp33str
    tempoutputyes=int(temphold,2)
    tempoutputyes=int2ba(tempoutputyes)   
    extend128(tempoutputyes,tempoutputyesyes)
    tempoutputyes=tempoutputyesyes[0]
    output.append(tempoutputyes)

    
def SerpentRun():
    LayerPInput=createinput()
    #LayerPInput2=''
    #LayerPInput2=IPFunctionInput(LayerPInput,LayerPInput2)
    ###if you do this one^, you need to change up how the next lines are done
    LayerPInput=SerpentRounds2(LayerPInput)
    print(LayerPInput)
    FinalWordFull=''
    FinalWordFull=str(LayerPInput)  #if you want it to run the FPFunction
    ##undo the # in front of it and add one to FinalWordFull=str(LayerPInput)
    #FinalWordFull=FPFunction(LayerPInput, FinalWordFull)
    FinalWordFull=FinalWordFull.replace("bitarray('",'')
    FinalWordFull=FinalWordFull.replace("')",'')
    FinalWordFullHex=hex(int(FinalWordFull,2))
    print("FinalWordFull: ",FinalWordFull)
    print("FinalWordFullHex: ",FinalWordFullHex)
    print(FinalWordFull,file=exampleoutput, end = "")
    return




   
    
ba = bitarray()
exampleoutput=open('exampleoutput.txt','w')
#f = open('exampletext.txt', 'rb')
#ba.fromfile(f)


#for i in range(0,128):
#        x = random.randint(0, 1)
#        ba.append(x)
#ba=bitarray('1100')
#print("File in bits: ",ba)
ba=bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

print("Length of File in bits: ",len(ba))
ba.reverse()
ba.fill()

#im sure this area is... odd
print("Length of File in bits: ",len(ba))

#print("File in bits: ",ba)

keyschedule()
#createinput()
#LayerPInput=RIRoundFunc(LayerPInput,0)


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

    
print("Execution Complete")
print("--- %s seconds ---" % (time.time() - start_time))
exampleoutput.close()


testingoutput=''
testingoutput2=''
LayerPInput=bitarray('10101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010')
testingoutput=IPFunction(LayerPInput,testingoutput)

testingoutput2=FPFunction(testingoutput, testingoutput2)

