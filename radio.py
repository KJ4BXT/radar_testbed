# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 01:30:58 2021

@author: Zac
"""

import matplotlib.pyplot as plt
import numpy as np
import adi

fs = 1e6 # MHz
center_freq = 100e6 # MHz
num_samps = 100000 # number of samples returned per call to rx()

sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 50.0 # dB, allowable range is 0 to 74.5 dB
sdr.rx_lo = int(center_freq)
sdr.sample_rate = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, adjust later
sdr.rx_buffer_size = num_samps

samples = sdr.rx() # receive samples off Pluto

#stuff below is redundant, copied from other file. Clean up later.

def waterfall(iq,n=1024):
    global freq_domain
    freq_domain = np.zeros((int(len(iq)/n),n))
    for i in range(int((len(iq-n)/n))):
        try:
            freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        except Exception:
            print('error')
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,fs/1e3,len(freq_domain),0],interpolation='nearest')


def waterfall2(iq,n=1024):
    global freq_domain
    #freq_domain = np.zeros((int(len(iq)),n))
    freq_domain = np.zeros(n)
    print(int(len(iq)))
    for i in range(int(len(iq))):
        print()
        #print((i+1)*n-i*n)
        #freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        #temp = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        temp = 10*np.log10(abs(np.fft.fft(iq[i:i+1+n],n)**2))
        #print(temp)
        freq_domain = np.vstack((freq_domain,temp))
        #if i > 5:
            #break
         #   continue
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,fs/2e6,len(freq_domain),0])#interpolation='nearest')
    #plt.plot(freq_domain[5])

waterfall(samples, 512)

plt.ion()
plt.show()