# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 22:18:11 2021

Signal generation and processing tests

@author: Zac
"""

import numpy as np
import matplotlib.pyplot as plt
%matplotlib qt
#%matplotlib inline

 #Signal generation and setup
# TODO: convert to complex (IQ) format
# TODO: have setup paramaters in a seperate file
fs = 10e6 # baseband sampling frequency. 10MHz startpoint
dur = .2 # length of simulation
t = np.arange(0,dur,1/int(fs))
freq = 1e6 # test signal freq. 0.3MHz CW startpoint
BW = 2.5e10
pulse_dur = 100e-6 # 10 us startpoint
pulse_len = int(fs*pulse_dur)
#source_sig = np.sin(np.array(t[:pulse_len])*np.pi*2*freq*(2.5+2.5*-np.cos(2*np.pi*BW*np.array(t[:pulse_len]))))
#source_sig = np.e**(1j*2*np.pi*freq*t[:pulse_len])
source_sig = np.e**(1j*2*np.pi*(freq + BW*t[:pulse_len])*t[:pulse_len])
window = np.kaiser(len(source_sig), 10)
pulse = source_sig#*window

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

#stuff below is redundant, copied from other file. Clean up later.
'''
def waterfall(iq,n=1024):
    global freq_domain
    freq_domain = np.zeros((int(len(iq)/n),n))
    for i in range(int((len(iq-n)/n))):
        try:
            freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        except Exception:
            print('error')
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,fs/1e6,len(freq_domain),0],interpolation='nearest')


def waterfall2(iq,n=1024):
    global freq_domain
    #freq_domain = np.zeros((int(len(iq)),n))
    freq_domain = np.zeros(n)
    print(int(len(iq)))
    for i in range(int(len(iq))):
        #print((i+1)*n-i*n)
        #freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        #temp = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        temp = 10*np.log10(abs(np.fft.fft(iq[i:i+1+n],n)**2))
        #print(temp)
        freq_domain = np.vstack((freq_domain,temp))
        if i > 5:
            #break
            continue
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,fs/2e6,len(freq_domain),0])#interpolation='nearest')
    #plt.plot(freq_domain[5])


waterfall2(pulse,1024)

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