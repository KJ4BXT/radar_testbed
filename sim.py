# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:18:11 2021

Signal generation and processing tests

@author: Zac
"""

import numpy as np
import matplotlib.pyplot as plt
#%matplotlib qt
#%matplotlib inline

 #Signal generation and setup
# TODO: convert to complex (IQ) format
fs = 10e6 # baseband sampling frequency. 10MHz startpoint
dur = .1 # length of simulation
t = np.arange(0,dur,1/int(fs))
freq = 3e6 # test signal freq. 0.3MHz CW startpoint
BW = 200
pulse_dur = 100e-6 # 10 us startpoint
pulse_len = int(fs*pulse_dur)
source_sig = np.sin(np.array(t[:pulse_len])*np.pi*2*freq*np.sin(2*np.pi*BW*np.array(t[:pulse_len])))
#source_sig = np.sin(np.array(t[:pulse_len])*np.pi*2*freq)

slice_dur = 0.01 # <- set this one
slice_len = int(slice_dur*fs)

# Generate RX signal(s)
noise = 1e-4
targets = [[800e-6,1e-2],[847e-6,1.3e-3],[1804e-6, 3.4e-2]] # range (time), amplitude
RX = noise*np.random.rand(int(fs*dur)) # Generates base noise floor
for i in targets:
    if ((i[0]*fs+pulse_len) > len(t)):
        raise Exception("target outside simulation range")
        continue
    RX = np.concatenate((RX[:int(i[0]*fs)],
                         RX[int(i[0]*fs)]+(source_sig*i[1]),
                         RX[int(i[0]*fs)+pulse_len:]))

# process received signals
# TODO: convert to FFT processing with scipy.signal.correlate for speed
DPC = np.zeros(len(t)) # Digital pulse compression vector
for i in range(len(t)):
    if ((i>pulse_len) and (i<(len(t)-pulse_len-1))): # Only process full returns
        DPC[i] = np.correlate(RX[i:i+pulse_len],source_sig)

#Graph stuff
plt.figure()
#plt.plot(t[:slice_len],source_sig[:slice_len])
#plt.plot(t[:slice_len],10*np.log10(abs(RX[:slice_len])))
plt.plot(t[:slice_len],10*np.log10(abs(DPC[:slice_len])))
plt.figure()
plt.plot(t[:len(source_sig)],source_sig)

plt.ion()
plt.show()
