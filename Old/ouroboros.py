import bitarray
from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba
from bitarray.util import zeros
from bitarray.util import serialize
from bitarray.util import ba2hex

#from bitarray import to01
import random
import numpy as np
import math
import galois

LayerPInput=[]
Player=[]
basekey=bitarray()
basekeyworking=[]
Key8wrds=[]
prekeyschedule=[]
prekeyschedulenibble=[]
prekeyschedulenibblesboxes=[]
keyschedulesboxes=[]
IP=[]
EP=[]
roundkeys=[]
SBoxKeyList=[3,2,1,0,7,6,5,4]
PlayerIPed=[]
fixedpermutationba=bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')
fixedpermutationba2=bitarray('00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000')

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

SBoxDecimalTable = [
	[ 3, 8,15, 1,10, 6, 5,11,14,13, 4, 2, 7, 0, 9,12 ], # S0
	[15,12, 2, 7, 9, 0, 5,10, 1,11,14, 8, 6,13, 3, 4 ], # S1
	[ 8, 6, 7, 9, 3,12,10,15,13, 1,14, 4, 0,11, 5, 2 ], # S2
	[ 0,15,11, 8,12, 9, 6, 3,13, 1, 2, 4,10, 7, 5,14 ], # S3
	[ 1,15, 8, 3,12, 0,11, 6, 2, 5, 4,10, 9,14, 7,13 ], # S4
	[15, 5, 2,11, 4,10, 9,12, 0, 3,14, 8,13, 6, 7, 1 ], # S5
	[ 7, 2,12, 5, 8, 4, 6,11,14, 9, 1,15,13, 3,10, 0 ], # S6
	[ 1,13,15, 0,14, 8, 2,11, 7, 4,12,10, 9, 3, 5, 6 ], # S7
    ] 
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


def ROR4(Input, RotationAmount):
    return (Input >> RotationAmount)|(Input << (4 - RotationAmount)) & 0xFFFFFFFF

def lshift(x, n):
    return ((x << n) & 0xFFFFFFFF) | (x >> (32 - n))

def rshift(x, n):
    return (x >> n) | ((x << (32 - n)) & 0xFFFFFFFF)

def createinput():
    if len(ba) > 128:
        x= slice(0,128)
        LayerPInput = (ba[x])
        del ba[0:128]
    elif len(ba) == 128:
        x= slice(0,128)
        LayerPInput = (ba[x])
        del ba[0:128]

    for i in range(0,4):
        tempSlice1 =LayerPInput[slice(0,8)]
        tempSlice2 =LayerPInput[slice(8,16)]
        tempSlice3 =LayerPInput[slice(16,24)]
        tempSlice4 =LayerPInput[slice(24,32)]
        LittleEndianByte= tempSlice4 +tempSlice3 + tempSlice2 + tempSlice1
        print("LittleEndianByte: ",LittleEndianByte)
        Player.append(LittleEndianByte)
        del LayerPInput[0:32]
    
    
def keygen():
    for i in range(0,256):
        x = random.randint(0, 1)
        basekey.append(x)
    print("Basekey: ",basekey)
    
def prekey():
    for i in range(0,132):
        #this section is a potential spot for errors/issues
        prekeygenerator1=Key8wrds[0]^Key8wrds[3]^Key8wrds[5]^Key8wrds[7]
        prekeygenerator2=prekeygenerator1^fracgoldratio^i
        prekeygenerator3=lshift(prekeygenerator2,11)
        
        #print("length of Prekeygenerator3: ",len(bin(prekeygenerator3)))
        prekeyschedule.append(prekeygenerator3)
        #it comes back weird cause it adds 0b on the front
        #could add a lengthen8multinsertfront here, but i would need to keep
        #it as a bitarray, which i dont like
            #prekeygenerator4=int2ba(prekeygenerator3)
            #if len(prekeygenerator4) < 32:
            #    prekeygenerator3=lengthen8multinsertfront
            #print("length of prekeygenerator4: ",len(prekeygenerator4))

def Sbox(inputnibble, outputnibble, Si):
    czz= inputnibble
    #print(czz)
    #print(Si)
    cff= serpentsboxes[Si][czz]
    cff=cff[0]
    ###or have  cff= SBoxDecimalTable[Si][czz]
    outputnibble.append(cff)


def SBoxKey(input3):
    for i in range(0,4):
        for n in SBoxKeyList:
            for i in range(0,8,2):
                tempstorage1=[]
                tempstorage2=[]
                Sbox(input3[i],tempstorage1,n)
                Sbox(input3[i+1],tempstorage2,n)
                batemp1=int2ba(tempstorage1[0])
                batemp2=int2ba(tempstorage2[0])
                lengthen8multinsertfront4(batemp1)
                lengthen8multinsertfront4(batemp2)
                batemp1str=str(batemp1[0])+str(batemp1[1])+str(batemp1[2])+str(batemp1[3])
                batemp2str=str(batemp2[0])+str(batemp2[1])+str(batemp2[2])+str(batemp2[3])
                tempstorage3=batemp1str+batemp2str
                keyschedulesboxes.append(tempstorage3)
                del input3[0:8]
            #gotta delete the input sections
    for i in range(0,8,2):
                tempstorage1=[]
                tempstorage2=[]
                Sbox(input3[i],tempstorage1,3)
                Sbox(input3[i+1],tempstorage2,3)
                batemp1=int2ba(tempstorage1[0])
                batemp2=int2ba(tempstorage2[0])
                lengthen8multinsertfront4(batemp1)
                lengthen8multinsertfront4(batemp2)
                batemp1str=str(batemp1[0])+str(batemp1[1])+str(batemp1[2])+str(batemp1[3])
                batemp2str=str(batemp2[0])+str(batemp2[1])+str(batemp2[2])+str(batemp2[3])
                tempstorage3=batemp1str+batemp2str
                keyschedulesboxes.append(tempstorage3)
                del input3[0:8]
    ##have to do it one more time with the first sbox i use

def roundkeymaker(input4, output): #input is keyscheduleboxes, output roundkeys
    for i in range(0,2): ###setup range to be 33 or 2
        temphold=input4[0]+input4[1]+input4[2]+input4[3]
        temphold=temphold+temphold+temphold+temphold
        del input4[0:4]
        print("Testing temphold",temphold)
        temphold2=IPRound(temphold)
        print("Testing temphold2",temphold2)
        output.append(temphold)
        print("Testing temphold",output)
    
        #creates 33 outputs, but it might only want 32
        ###i...dont know why the IPRound makes it into a string but ill take it?
def keyschedule():
    keygen()
    basekeyworking = basekey.copy()
    for i in range(0,8):
        tempSlice1 =basekeyworking[slice(0,32)]
        tempSlice1=ba2int(tempSlice1)
        Key8wrds.append(tempSlice1)
        #print(type(Key8wrds[i]))
        del basekeyworking[0:32]
    prekey()
    #print("PrekeyScheduleType: ",type(prekeyschedule))
    #print("prekeyschedule : ",prekeyschedule)
    #print("prekeyschedule[0] : ",prekeyschedule[0])
    #print("PrekeyScheduleType: ",type(prekeyschedule[0]))
    nibbleslice(prekeyschedule, prekeyschedulenibble,132, 32)
    #print(prekeyschedulenibble)

    #print("prekeyschedulenibble test: ",prekeyschedulenibble)
    SBoxKey(prekeyschedulenibble)
    roundkeymaker(keyschedulesboxes, roundkeys)



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
    else:
        Input.append(0)
    Input.reverse()
def nibbleslice(Input, inputnibble,length, length2):
    #print("Input: ",input)
    for n in range(0,length): #replace the second number with len(input)
        tempb4nibble=Input[n]
        tempb4nibbleba=int2ba(tempb4nibble)
        if len(tempb4nibbleba) < length2:
            tempb4nibble=lengthen8multinsertfront(tempb4nibbleba)   

    #i am concerned about how serpent wants us to make the 4 bit input into
    #sboxes. Im rather confused about it and could be an easy thing to get wrong

        tempnibble1=ba2int(tempb4nibbleba[slice(0,4)])
        tempnibble2=ba2int(tempb4nibbleba[slice(4,8)])
        tempnibble3=ba2int(tempb4nibbleba[slice(8,12)])
        tempnibble4=ba2int(tempb4nibbleba[slice(12,16)])
        tempnibble5=ba2int(tempb4nibbleba[slice(16,20)])
        tempnibble6=ba2int(tempb4nibbleba[slice(20,24)])
        tempnibble7=ba2int(tempb4nibbleba[slice(24,28)])
        tempnibble8=ba2int(tempb4nibbleba[slice(28,32)])
        inputnibble.append(tempnibble1)
        inputnibble.append(tempnibble2)
        inputnibble.append(tempnibble3)
        inputnibble.append(tempnibble4)
        inputnibble.append(tempnibble5)
        inputnibble.append(tempnibble6)
        inputnibble.append(tempnibble7)
        inputnibble.append(tempnibble8)
         

    
def permutationserp2(ReferenceTable,Input,Output):
    for i in range(0,128):
        cz= ReferenceTable[i]
        cf= int(Input[cz])
        fixedpermutationba2[i]=cf
    Output.append(fixedpermutationba)

def permutationserp(ReferenceTable,Input,Output):
    for i in range(0,128):
        cz= ReferenceTable[i]
        cf= int(Input[cz])
        fixedpermutationba[i]=cf
    Output.append(fixedpermutationba)

def IPRound(Input2):
    permutationserp(IPTable, Input2, IP)
    Input2=IP
    return IP
    
def IPRoundPlaintext(Input2, Output2):
    print(IP)
    permutationserp2(IPTable, Input2, IP)
    Input2=IP
    Output2.append(Input2)


##area significantly weird... but timecrunch and it works
def FPRound(Input2, Output2):
    permutationserpPlaintext(FPTable, Input2, EP)
    Input2=EP
    Output2.append(Input2)
    #print("FPRound")   


        
def SerpentRounds(Input):
    for i in range(0,3):
        print(i)
        EightRIRoundFunc(Input)
    for i in range(0,7):
       RIRoundFunc(Input, i)
    ###add in last round(s)
       ###add in thing for after last round

def EightRIRoundFunc(Input):
    for i in range(0,8):
        RIRoundFunc(Input, i)



Playerinputnibble=[]
Playeroutputnibble=[]
def RIRoundFunc(Input,inputnibble,outputnibble, Round):
    #Input=int2ba(Input)
    #Input=ba2int(Input)
    print("Input",Input)
    nibbleslice(Input, inputnibble,4, 32)
    print(inputnibble)
    print(len(inputnibble))
    for i in range(0,32):
        Sbox(inputnibble, outputnibble, Round)
    print(Input)
    ###Ri(X) = L(Sˆi(X ⊕ Kˆi)) i = 0,..., 30
    ##tempstorage=Input[0]^Key8wrds[3]^Key8wrds[5]^Key8wrds[7]

#### setup last round func
def LastRoundFunc(Input,Output):
    print(Input)
    ###Ri(X) = Sˆi(X ⊕ Kˆi) ⊕ Kˆ32 i = 31
    
ba = bitarray(endian='little')
exampleoutput=open('exampleoutput.txt','w')
f = open('exampletext.txt', 'rb')
ba.fromfile(f)

print("Length of File in bits: ",len(ba))
createinput()
Player=Player[0]+Player[1]+Player[2]+Player[3]
#print("Player", ba2hex(Player))
keyschedule()
del IP
IP=[]
Player=IPRoundPlaintext(Player,PlayerIPed)
PlayerIPed=PlayerIPed[0][0]
print("PlayerIPed",PlayerIPed)
tempSlice1 =ba2int(PlayerIPed[slice(0,32)])
tempSlice2 =ba2int(PlayerIPed[slice(32,64)])
tempSlice3 =ba2int(PlayerIPed[slice(64,96)])
tempSlice4 =ba2int(PlayerIPed[slice(96,128)])
del PlayerIPed
PlayerIPed=[]
PlayerIPed.append(tempSlice1)
PlayerIPed.append(tempSlice2)
PlayerIPed.append(tempSlice3)
PlayerIPed.append(tempSlice4)
print("PlayerIPed b4 int: ",PlayerIPed)
print(type(PlayerIPed))
RIRoundFunc(PlayerIPed,Playerinputnibble,Playeroutputnibble, 0)
