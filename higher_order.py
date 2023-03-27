import random

'''
Some useful real S-boxes.
'''

Serpent_subL = {'boxes': 8, 'length': 16}
Serpent_s0box = [
[3,8,15,1,10,6,5,11,14,13,4,2,7,0,9,12], \
[15,12,2,7,9,0,5,10,1,11,14,8,6,13,3,4], \
[8,6,7,9,3,12,10,15,13,1,14,4,0,11,5,2], \
[0,15,11,8,12,9,6,3,13,1,2,4,10,7,5,14], \
[1,15,8,3,12,0,11,6,2,5,4,10,9,14,7,13], \
[15,5,2,11,4,10,9,12,0,3,14,8,13,6,7,1], \
[7,2,12,5,8,4,6,11,14,9,1,15,13,3,10,0], \
[1,13,15,0,14,8,2,11,7,4,12,10,9,3,5,6]]

AES_subL = {'boxes': 1, 'length': 256}
AES_s0box = [[
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]]

'''
-----------------------
-CREATE MASKED S-BOXES-
-----------------------
'''

''' set up which S-boxes to use '''
#subL = AES_subL
#s0box = AES_s0box
subL = Serpent_subL
s0box = Serpent_s0box
''' end of setup '''

s1box = [[[] for i in range(subL['length'])] for j in range(subL['boxes'])]
s2box = [[[[] for i in range(subL['length'])] for j in range(subL['length'])] for k in range(subL['boxes'])]
#s3box = [[[[[]]]]]
''' comment s3box for AES, it is too slow and large (4GB) '''
s3box = [[[[[] for i in range(subL['length'])] for j in range(subL['length'])] for k in range(subL['length'])] for l in range(subL['boxes'])]
''' comment s4box for AES, it is too slow and large (1TB) '''
s4box = [[[[[[] for i in range(subL['length'])] for j in range(subL['length'])] for k in range(subL['length'])] for l in range(subL['length'])] for m in range(subL['boxes'])]

for box in range(subL['boxes']):

     for r0 in range(subL['length']):
          for kxd in range(subL['length']):
             s1box[box][r0].append( s0box[box][kxd] ^ s0box[box][kxd^r0] )



     for r1 in range(subL['length']):
          for r0 in range(subL['length']):
               for kxd in range(subL['length']):
                    s2box[box][r0][r1].append( s0box[box][kxd^r0] ^ s0box[box][kxd^r0^r1] )

     ''' comment s3box for AES, it is too slow and large (4GB) '''
     for r2 in range(subL['length']):
          for r1 in range(subL['length']):
               for r0 in range(subL['length']):
                    for kxd in range(subL['length']):
                         s3box[box][r0][r1][r2].append( s0box[box][kxd^r0^r1] ^ s0box[box][kxd^r0^r1^r2] )
 
     ''' comment s4box for AES, it is too slow and large (1TB) '''
     for r3 in range(subL['length']):
          for r2 in range(subL['length']):
               for r1 in range(subL['length']):
                    for r0 in range(subL['length']):
                         for kxd in range(subL['length']):
                              s4box[box][r0][r1][r2][r3].append( s0box[box][kxd^r0^r1^r2] ^ s0box[box][kxd^r0^r1^r2^r3] )
 
'''
---------------
-CHECK S-BOXES-
---------------
'''

def S1m(box, kxd, r0):
     share0 =     s0box[box][kxd^r0]
     share1 = s1box[box][r0][kxd^r0]
     return share0 ^ share1
     
def S2m(box, kxd, r0, r1):
     share0 =         s0box[box][kxd^r0^r1]
     share1 =     s1box[box][r0][kxd^r0]
     share2 = s2box[box][r0][r1][kxd^r1]
     return share0 ^ share1 ^ share2
 
def S3m(box, kxd, r0, r1, r2):
     share0 =             s0box[box][kxd^r0^r1^r2]
     share1 =         s1box[box][r0][kxd^r0]
     share2 =     s2box[box][r0][r1][kxd^r1]
     share3 = s3box[box][r0][r1][r2][kxd^r2]
     return share0 ^ share1 ^ share2 ^ share3

def S4m(box, kxd, r0, r1, r2, r3):
     share0 =                 s0box[box][kxd^r0^r1^r2^r3]
     share1 =             s1box[box][r0][kxd^r0]
     share2 =         s2box[box][r0][r1][kxd^r1]
     share3 =     s3box[box][r0][r1][r2][kxd^r2]
     share4 = s4box[box][r0][r1][r2][r3][kxd^r3]
     return share0 ^ share1 ^ share2 ^ share3 ^ share4
 
# checking for a few arbitrary values

testL = 5
t = [[random.randint(0,subL['length']-1) for _ in range(testL)] for _ in range(4)]
for box in range(subL['boxes']):
     
     print('Box:', box)
                
     correct = True
     for kxd in t[0]:
          for r0 in t[1]:
               if S1m(box, kxd, r0) != s0box[box][kxd]:
                              correct = False
     print('1st Mask-BOX correct:', correct)       

     correct = True
     for kxd in t[0]:
          for r0 in t[1]:
               for r1 in t[2]:
                    if S2m(box, kxd, r0, r1) != s0box[box][kxd]:
                              correct = False
     print('2nd Mask-BOX correct:', correct)

     ''' comment s3box for AES, it is too slow and large (4GB) '''                 
     correct = True
     for kxd in t[0]:
          for r0 in t[1]:
               for r1 in t[2]:
                    for r2 in t[2]:
                         if S3m(box, kxd, r0, r1, r2) != s0box[box][kxd]:
                                   correct = False
     print('3rd Mask-BOX correct:', correct)
                   
     ''' comment s4box for AES, it is too slow and large (1TB) '''          
     correct = True
     for kxd in t[0]:
          for r0 in t[1]:
               for r1 in t[2]:
                    for r2 in t[2]:
                         if S4m(box, kxd, r0, r1, r2, r3) != s0box[box][kxd]:
                                   correct = False
     print('4th Mask-BOX correct:', correct)
                   
'''
-----------------------
-SIMULATE MEASUREMENTS-
-----------------------
'''
# Hamming weight of x
def hamW(x):
    y = 0
    while(x>0):
        y+=(x&1)
        x>>=1
    return y

'''
---------
-HACK IT-
---------
'''






