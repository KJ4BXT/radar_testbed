# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 01:30:58 2021

This file handles the receive and transmit 
and a whole lot more until I clean it up

@author: Zac
"""

import matplotlib.pyplot as plt
import numpy as np
#from time import sleep
import adi

fs = 50e6 # Hz
center_freq = 5700e6 # Hz
num_samps = 500000 # number of samples returned per call to rx()

sdr = adi.Pluto()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 40 # dB
sdr.rx_lo = int(center_freq)
sdr.fs = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, just set it to the same as sample rate for now
sdr.rx_buffer_size = num_samps

sdr.tx_rf_bandwidth = int(fs) # filter cutoff, just set it to the same as sample rate
sdr.tx_lo = int(center_freq)
sdr.tx_hardwaregain_chan0 = -10 # Increase to increase tx power, valid range is -90 to 0 dB

N = 50000 # number of samples to transmit at once
t = np.arange(N)/fs
pulse = 0.5*np.exp(2.0j*np.pi*2.5e10*t*t) #TODO: Remove hardcoded value

source_mod = 0.25*np.cos(-2*np.pi*1800*t)+0.75
source_sig = 0.5*np.exp(2.0j*np.pi*(source_mod)*t*fs)

window = np.kaiser(len(pulse), 20)
#pulse *= window
source_sig = np.concatenate((pulse,np.zeros(len(pulse))))
source_sig *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs
sdr.tx_cyclic_buffer = True # Enable cyclic buffers


sdr.tx(source_sig) # transmit the batch of samples once


RX = sdr.rx() # receive samples off Pluto
sdr.tx_destroy_buffer()

#stuff below is redundant, copied from other file. Clean up later.
np.seterr(divide = 'ignore') # This is a hack and bad and you shouldn't do it 

DPC = abs(np.correlate(RX,pulse))
DPC *= 1/max(DPC)

slice_len = -1

plt.figure()
#plt.plot(t[:slice_len],10*np.log10(abs(DPC[:slice_len])))
plt.plot(10*np.log10(DPC))

plt.ion()
plt.show()