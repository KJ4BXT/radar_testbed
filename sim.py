# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:18:11 2021

Signal generation and processing tests

@author: Zac
"""

import numpy as np
import matplotlib.pyplot as plt
import graphing as g

#%matplotlib qt

 #Signal generation and setup
# TODO: convert to complex (IQ) format
# TODO: have setup paramaters in a seperate file
fs = 50e6 # baseband sampling frequency. 50MHz
dur = 200e-6 # length of simulation. About 20 miles - pulse length. 200us
freq = 0 # test signal freq.
BW = 15e11 # I have no idea if this has useful units
#pulse_dur = 0.0005 # 10 ms startpoint
#pulse_len = int(fs*pulse_dur)

N = 1e3 # number of pulse samples
#pulse_t = np.arange(int(dur*fs))/fs
pulse_t = np.arange(N)/fs

t = np.arange(0,dur,1/int(fs))

source_mod = 0.25*np.cos(-2*np.pi*1800*pulse_t)+0.75

#source_sig = np.sin(np.array(t[:pulse_len])*np.pi*2*freq*(2.5+2.5*-np.cos(2*np.pi*BW*np.array(t[:pulse_len]))))
#source_sig = np.e**(1j*2*np.pi*freq*t[:pulse_len])
#source_sig = np.e**(1j*2*np.pi*(freq + BW*t[:pulse_len])*t[:pulse_len])
source_sig = 0.5*np.exp(2.0j*np.pi*(freq+BW*pulse_t)*pulse_t)
#source_sig = 0.5*np.exp(2.0j*np.pi*2.4e7*pulse_t)
#source_sig = 0.5*np.exp(2.0j*np.pi*(source_mod)*pulse_t*fs)

window = np.kaiser(len(source_sig), 10)
pulse = source_sig*window

g.waterfall(pulse,128)


slice_dur = 0.05 # <- set this one
slice_len = int(slice_dur*fs)

# Generate RX signal(s)
noise = 1e-4
targets = [[110e-6,1e-1],[163e-6,1.3e-3],[50e-6, 3.4e-2]] # range (time), amplitude
RX = noise*np.random.rand(int(fs*dur)) # Generates base noise floor
for i in targets:
    if ((i[0]*fs+len(pulse)) > len(t)):
        raise Exception("target outside simulation range")
        continue
    RX = np.concatenate((RX[:int(i[0]*fs)],
                         RX[int(i[0]*fs)]+(pulse*i[1]),
                         RX[int(i[0]*fs)+len(pulse):]))
'''
dec = 1 #decimate
# process received signals
# TODO: convert to FFT processing with scipy.signal.correlate for speed
DPC = np.zeros(len(t)) # Digital pulse compression vector
for i in range(int(len(t)/dec-1)):
    i *= dec
    #print(i,'of ',int(len(t)/dec))
    if ((i>len(pulse)) and (i<(len(t)-len(pulse)-1))): # Only process full returns
    # if ((i>len(pulse)/2) and (i<(len(t)-len(pulse)/2-1))):
        tmp = np.correlate(RX[i:i+len(pulse)],pulse)
        #print(tmp)
        if i%1000 == 0:
            print(i,'of ',int(len(t)))
        DPC[i] = sum(tmp.real)

'''

DPC = abs(np.correlate(RX,pulse))

#to keep the log graph from throwing up, should probably do something better
DPC += np.random.random(len(DPC))*1e-10



#Graph stuff
plt.figure()
#plt.plot(t[:slice_len],pulse.real[:slice_len])
#plt.plot(t[:slice_len], pulse.imag[:slice_len])
#plt.plot(t[:slice_len],10*np.log10(abs(RX[:slice_len])))
plt.plot(g.radar_distance(t[:len(DPC)]),10*np.log10(abs(DPC)))
'''
plt.figure()

plt.plot(pulse_t,source_mod)

plt.ion()
plt.show()
'''