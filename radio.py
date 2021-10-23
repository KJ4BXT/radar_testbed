# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 01:30:58 2021

@author: Zac
"""

import matplotlib.pyplot as plt
import numpy as np
import graphing as g
#from time import sleep
import adi

fs = 1e6 # Hz
center_freq = 100e6 # Hz
num_samps = 10000 # number of samples returned per call to rx()

sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 50.0 # dB
sdr.rx_lo = int(center_freq)
sdr.fs = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

sdr.tx_rf_bandwidth = int(fs) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -50 # Increase to increase tx power, valid range is -90 to 0 dB

N = 10000 # number of samples to transmit at once
t = np.arange(N)/fs
samples = 0.5*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz
samples2 = 0.5*np.exp(2.0j*np.pi*900e3*t) # Simulate a sinusoid of 100 kHz
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
sdr.tx_cyclic_buffer = True # Enable cyclic buffers


sdr.tx(samples) # transmit the batch of samples once


RX = sdr.rx() # receive samples off Pluto
sdr.tx_destroy_buffer()

#stuff below is redundant, copied from other file. Clean up later.
np.seterr(divide = 'ignore') # This is a hack and bad and you shouldn't do it

'''
DPC = np.zeros(len(RX)) # Digital pulse compression vector
for i in range(len(RX)-1):
    if ((i>len(pulse)) and (i<(len(RX)-len(pulse)-1))): # Only process full returns
        DPC[i] = np.correlate(RX[i:i+len(pulse)],pulse)[0]
'''

g.waterfall(RX, 128)
#waterfall(pulse, 256)

#plt.figure()
#plt.plot(t[:slice_len],10*np.log10(abs(DPC[:slice_len])))


plt.ion()
plt.show()