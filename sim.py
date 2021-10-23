# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:18:11 2021

Signal generation and processing tests

@author: Zac
"""

import numpy as np
import matplotlib.pyplot as plt
import graphing as g

 #Signal generation and setup
# TODO: convert to complex (IQ) format
# TODO: have setup paramaters in a seperate file
fs = 1e6 # baseband sampling frequency. 10MHz startpoint
dur = .5 # length of simulation
freq = 0 # test signal freq. 0.3MHz CW startpoint
BW = 5e7
pulse_dur = 0.0005 # 10 ms startpoint
pulse_len = int(fs*pulse_dur)

N = 1e4 # number of pulse samples
t = np.arange(N)/fs

#source_sig = np.sin(np.array(t[:pulse_len])*np.pi*2*freq*(2.5+2.5*-np.cos(2*np.pi*BW*np.array(t[:pulse_len]))))
#source_sig = np.e**(1j*2*np.pi*freq*t[:pulse_len])
#source_sig = np.e**(1j*2*np.pi*(freq + BW*t[:pulse_len])*t[:pulse_len])
source_sig = 0.5*np.exp(2.0j*np.pi*(freq+BW*t)*t) # Simulate a sinusoid of 100 kHz

window = np.kaiser(len(source_sig), 10)
pulse = source_sig*window

slice_dur = pulse_dur # <- set this one
slice_len = int(slice_dur*fs)

# Generate RX signal(s)
noise = 1e-4
targets = [[800e-6,1e-2],[864e-6,1.3e-3],[1804e-6, 3.4e-2]] # range (time), amplitude
RX = noise*np.random.rand(int(fs*dur)) # Generates base noise floor
for i in targets:
    if ((i[0]*fs+pulse_len) > len(t)):
        raise Exception("target outside simulation range")
        continue
    RX = np.concatenate((RX[:int(i[0]*fs)],
                         RX[int(i[0]*fs)]+(pulse*i[1]),
                         RX[int(i[0]*fs)+pulse_len:]))
'''
# process received signals
# TODO: convert to FFT processing with scipy.signal.correlate for speed
DPC = np.zeros(len(t)) # Digital pulse compression vector
for i in range(len(t)):
    if ((i>pulse_len) and (i<(len(t)-pulse_len-1))): # Only process full returns
        DPC[i] = np.correlate(RX[i:i+pulse_len],pulse)

'''

g.waterfall(pulse,256)

#Graph stuff
#plt.figure()
#plt.plot(t[:slice_len],pulse.real[:slice_len])
#plt.plot(t[:slice_len], pulse.imag[:slice_len])
#plt.plot(t[:slice_len],10*np.log10(abs(RX[:slice_len])))
# plt.plot(t[:slice_len],10*np.log10(abs(DPC[:slice_len])))
# plt.figure()

#plt.plot(t[:len(pulse)],pulse)

plt.ion()
plt.show()