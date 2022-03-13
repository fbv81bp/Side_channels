'''
Mutual Information Analysis LIKE* practice on AES S-box based on Hamming distances:
multiple bytes implementation, where at hacking a specific input byte, all other
byte substitutions represent algorithmic noise

(*) As I interpret Shannon entropy based MIA, it is something like finding out if
the probability distribution ie. the frequencies of output samples relate to choosen
input data as expected. I left out logarithm for example, because it is a monothonic
function, summing up logarithms has to have the same correlation results as just plain
numbers. I rather gather the corresponding leakage to every plain text value. Now since
all leakages are between 0 to 8 per S-box output, while there are 65536 possible plain
text switchings, the matching is between which plain text switch causes what amount of
leakage with a certain key assumed.
As for the results, roughly the same amount of samples are needed for a proper key
recovery, but the calculation got a lot faster compared to CPA SCA.
'''

import random
import time

s_box = [
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
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]

# Hamming weight of x
def count1s(x):
    y = 0
    while(x>0):
        y+=(x&1)
        x>>=1
    return y

'''
-----------------------
-SIMULATE MEASUREMENTS-
-----------------------
'''

# number of choosen plain texts
number_of_traces = 1000
print('Number of traces:', number_of_traces)

# number of parallel S-box computations
S_box_count = 16
print('S-box count:', S_box_count)

# picking a set of random keys
key_bytes = [random.randint(0,255) for i in range(S_box_count)]

# picking random input data sets
choosen_plain_texts = [[random.randint(0,255) for j in range(number_of_traces)] for i in range(S_box_count)]

# calculating leakages
leakages = [0 for i in range(number_of_traces-1)]
for tr in range(number_of_traces-1):
    for sb in range(S_box_count):
            leakages[tr] += count1s(s_box[key_bytes[sb] ^ choosen_plain_texts[sb][tr+1]]) - count1s(s_box[key_bytes[sb] ^ choosen_plain_texts[sb][tr]])

'''
---------
-HACK IT-
---------
'''

#calculating something like mutual information
most_likely_keys = [None for i in range(S_box_count)]

# setting up probability masses of leakages with respect to choosen plain text switchings: each plain text switch should trigger a certain
# amount of leakage, so summing up leakages at given plain text value pairs gives a distribution characteristic to the key

# loop through all inputs
for key_idx in range(S_box_count):
    print('Guessing Key #',key_idx, 'started at', time.time())

    # assigning leakages to their respective(*) choosen plain text byte pair and simultaneously summing up the corresponding leakage values
    histogram_like_stuff = [[0 for plain0 in range(256)] for plain1 in range(256)] # neither histogram, nor a probability mass, as described in line 10
    for tr in range(number_of_traces-1):
        histogram_like_stuff[choosen_plain_texts[key_idx][tr+1]][choosen_plain_texts[key_idx][tr]] += leakages[tr]

    # loop through all keys and find best matching between of "histogram" and hypothesises
    current_likely_key = 0
    highest_correlation = 0
    for assumed_key in range(256):

        # only computing the relevant parts of hypothesises to spare time: for the particular key, and with the particular choosen plain text transitions
        hypothesises = [[0 for plain0 in range(256)] for plain1 in range(256)]
        for tr in range(number_of_traces-1):
                plain0 = choosen_plain_texts[key_idx][tr]
                plain1 = choosen_plain_texts[key_idx][tr+1]
                hypothesises[plain1][plain0] = count1s(s_box[plain1 ^ assumed_key]) - count1s(s_box[plain0 ^ assumed_key])

        correlation = 0
        for plain0 in range(256):
            for plain1 in range(256):
                # (*) it is vital, that all S-boxes have different and known choosen plain text series, which result in different histograms
                correlation += hypothesises[plain1][plain0] * histogram_like_stuff[plain1][plain0]
            if correlation > highest_correlation:
                highest_correlation = correlation
                current_likely_key = assumed_key
    most_likely_keys[key_idx] = current_likely_key

print('Done at', time.time())
print()
print('   Real keys:', key_bytes)
print('Guessed keys:', most_likely_keys)


