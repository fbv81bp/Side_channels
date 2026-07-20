'''
This is a very simplistic basic test of my concept about hacking modular adders:
adders cause a monothonic and circulat "delay" in a monothonically increasing
input sequence. Thus if we manage to drive the adder's controlled input with a
monothon increasing input sequence, then the leakage's delay compared to the
controlled input's Hamming weight, will give the secret number that the adder is
adding to the sequence over mod(256).

There is more to it, like starting from MSB where carry doesn't matter, and then
correcting with the guessed higher bytes' for the lower ones: when a carry ripples
through into higher positions. Also, a sequence of ...010000000b is easily
mistaken for 0 as that 1 just moves one bit higher during half of the sequence.
'''

import random
secret32 = random.randint(0, 2**32-1)
secret32 = 0x128043ab # this gives a fault at 8...
print(hex(secret32))

trace_length = 3*256

def hamming_weight(x):
    w = 0
    while x > 0:
        w += (x%2)
        x //=2
    return w

# initializing hypothetical trace
expected_trace = [hamming_weight(i%256) for i in range(trace_length)]

# looping from MSbyte to LSbyte, because MSbyte has no carry out effects
keys = [0, 0, 0, 0]
known_secret = 0
for byte_idx in range(4):
    
    # expected trace should be aligned with suspected higher bytes' values in
    # case of carry overflow... except for the overflow depends on the next yet
    # secret value(!) - but it is seemingly unnecessary: the carry adds a fixed
    # offset above the shift value, but correlation is not disturbed by that(?!!)
    
    # apparantly it mixes up 0x0 with 0x8 very easily...
    
    # simulating traces
    trace = []
    for trace_idx in range(trace_length):
        plain = trace_idx%256
        trace.append(hamming_weight(secret32 + (plain*(256**byte_idx))))
    
    # looking for the shift with the highest correlation: giving back the secret byte
    max_correlation = 0
    for shift_in_correlation in range(256):
        shift_correlation = 0
        for corr_idx in range(trace_length):
            shift_correlation += (expected_trace[corr_idx] * trace[corr_idx-shift_in_correlation])
        if shift_correlation > max_correlation:
            max_correlation = shift_correlation
            keys[byte_idx] = shift_in_correlation
    known_secret += (keys[byte_idx] * 256**byte_idx)

print(hex(known_secret))
