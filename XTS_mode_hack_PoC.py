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

def hamming_weight(x):
    i = 0
    while x > 0:
        i += x % 2
        x //= 2
    return i

'''

instead of guessing 1 single key byte, we begin with two, which takes 65536 combinations, which is still
bearable; in case the 2 byte plain text would knock out the key bytes at the given position to zero, then
we get at every 8th encryption step, the higher sub-bytes will consume just as much energy, as the lower
sub-bytes 8 encryptions before: that is because at every step, the mask is multiplied by just two, ie. shifed
left over most of the key space...

so once we get a high correlation with a shift of 8, we guessed the two bytes well

btw. any ofthe 65536 will be provide this high self correlation of the power trace, that unmasks the two key
bytes to be identical, not just both 0... so there will be 256 possible values for every two bytes left, which
can then be iterated by shifting the guess window by just 1 byte...

well giving it more thoughts, this method searches for the XOR difference between consecutive key bytes, so
a 256 strong per key-byte-pair search space is enough! then what remains unknown is the last key byte's relation
to the MSB byte, the LSB, as we do not know when the Galois field modulus is XOR-ed on its mask, so that is a
bit unreliable, but we are going to know all the XOR differences between all key bytes from MSB downto LSB, and
we will have an unknown 'offset' like value, namely what may be an actual key byte anywhre, that is then XOR-ed
to have all other key bytes: this makes up 6x256 trials measurent sequences, and 1x256 key trials in the end!

'''

# Proof of Concept of the correlation working

trace_length = 520 # 512 + 8
trace = []

from random import randint as rdi

init = rdi(0,65535) # mask that is shifted from right with single bit random values

for run in range(trace_length):
        initL = init & 0xFF
        initH = (init >> 8) & 0xFF
        weight_sum = hamming_weight(s_box[initL]) + hamming_weight(s_box[initH])
        trace.append(weight_sum)
        init *=2
        init += rdi(0,1)
        init %= 65536

# test for period
shift_hist = []

mean = 0
for t in trace:
    mean += t
mean /= trace_length

vari = []
for t in trace:
    vari.append(t-mean)


for shift in range(1,16):
    self_corr = 0
    for i in range(trace_length - shift):
        self_corr += (vari[i] * vari[i + shift])
        #self_corr += (trace[i] * trace[i + shift])
    self_corr /= (trace_length - shift)
    shift_hist.append(self_corr)
    
for s in shift_hist:
    print(s)

# Test that there is no correlation if the key bytes weren't XOR-ed to match

mismatch = rdi(0,255)
print(mismatch)

trace_length = 520 # 512 + 8
trace = []

from random import randint as rdi

init = rdi(0,65535) # mask that is shifted from right with single bit random values


for run in range(trace_length):
        initL = init & 0xFF
        initL ^= mismatch
        initH = (init >> 8) & 0xFF
        weight_sum = hamming_weight(s_box[initL]) + hamming_weight(s_box[initH])
        trace.append(weight_sum)
        init *=2
        init += rdi(0,1)
        init %= 65536

# test for period
shift_hist = []

mean = 0
for t in trace:
    mean += t
mean /= trace_length

vari = []
for t in trace:
    vari.append(t-mean)


for shift in range(1,16):
    self_corr = 0
    for i in range(trace_length - shift):
        self_corr += (vari[i] * vari[i + shift])
        #self_corr += (trace[i] * trace[i + shift])
    self_corr /= (trace_length - shift)
    shift_hist.append(self_corr)
    
for s in shift_hist:
    print(s)
print()
