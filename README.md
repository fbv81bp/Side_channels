# Side_channel_attacks
* Hweight_dpa_sca_aes_sbox.py : A schoolbook example of differential power analysis side channel analysis of Advanced Encryption Standard's S-box based hacking.
* Hdist_dpa_sca_aes_sbox.py : Roughly the same, but with Hamming distances being considered as the primary leakage source.
* Hweight_dpa_sca_16x_aes_sbox.py : A more near life solution where multiple S-box computations comprise the leakage. As such, the example also shows, that this attack works in the presence of noise, because when the input of a particular S-box is being guessed, all other S-box substitutions are meaningless (algorithmic) noise in the leakage data.
