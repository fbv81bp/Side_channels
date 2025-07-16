from random import randint as rdi
import matplotlib.pyplot as plt

sbox_size = 256

# create a randomized sbox
sbox = [i for i in range(sbox_size)]
for _ in range(20 * sbox_size):
    r = rdi(0, len(sbox) - 1)
    sbox[0], sbox[r] = sbox[r], sbox[0]

# collect data with extremal power consumption according to hypothetical keys
keys = sbox_size

# collect 16 data input for every possible key with minimal and maximal hamming weights
extreme_data_per_key = [[[],[]] for _ in range(keys)]

def hamming_weight(x):
    i = 0
    while x > 0:
        i += x % 2
        x //= 2
    return i

for key in range(keys):
    for data_in in range(keys):
        data_out = sbox[key ^ data_in]
        if hamming_weight(data_out) < 3:
            extreme_data_per_key[key][0].append(data_in) # minimal Hamming weights
        if hamming_weight(data_out) > 5:
            extreme_data_per_key[key][1].append(data_in) # maximal Hamming weights

# simulate power consumptions with a particular key
real_key = rdi(0,255)

trace_length = 2000

# adjusts period in power consumtion so that it may penetrate supply filtering(!)
period = 50

# making the power consumption to have a pattern that is really obvious if recognized
# perhaps this could even be the 8b/10b encoded pattern of the key assumption, so that
# the appearing, arising shape in the power trace directly signals what the real key
# is as found - much futher improvements might add a simple LFSR so that the observation
# isn't so obvious for the system owner if they were to expect the attack... etc.
encoding = [0,1,1,0,1,1,0,0,0,1,0]

power_traces = [[] for _ in range (keys)]

for hypothetical_key in range(keys):
    for trace_index in range(trace_length):
        hamming_index = encoding[trace_index // period % len(encoding)]
        data = extreme_data_per_key[hypothetical_key][hamming_index][rdi(0, 24)]
        power_traces[hypothetical_key].append(hamming_weight(sbox[real_key^data]))

x = [i for i in range(trace_length)]

# plot power trace with the right key
plt.plot(x, power_traces[real_key])
plt.show()

# plot some traces created by driving with data associated with a wrong key assumption
for _ in range(3):
    plt.plot(x, power_traces[rdi(0,keys - 1)])
    plt.show()
