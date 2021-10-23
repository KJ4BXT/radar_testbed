# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 01:30:58 2021

@author: Zac
"""

import matplotlib.pyplot as plt
import numpy as np
import graphing as g
import adi

fs = 1e6 # MHz
center_freq = 5700e6 # MHz
num_samps = 1e6 # number of samples returned per call to rx()

dur = .2 # length of simulation, need to change to pulse based?
t = np.arange(0,dur,1/int(fs))
freq = 0.2e6 # test signal freq. 0.3MHz CW startpoint
BW = 0.3e9
pulse_dur = 0.0005 # 10 us startpoint
pulse_len = int(fs*pulse_dur)

sdr = adi.Pluto()
sdr.tx_destroy_buffer()
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 5.0 # dB, allowable range is 0 to 74.5 dB
sdr.rx_lo = int(center_freq)
sdr.tx_lo = int(center_freq)
sdr.sample_rate = int(fs)
sdr.rx_rf_bandwidth = int(fs) # filter width, adjust later
sdr.tx_hardwaregain_chan0 = -50 # Increase to increase tx power, valid range is -90 to 0 dB
sdr.tx_cyclic_buffer = True # Enable cyclic buffers
sdr.rx_buffer_size = num_samps

slice_dur = dur # <- set this one
slice_len = int(slice_dur*fs)

#sample code from site
num_symbols = 1000
source_sig = np.e**(1j*2*np.pi*(freq + BW*t[:pulse_len])*t[:pulse_len])
#source_sig = np.e**(1j*2*np.pi*freq*t[:pulse_len])
window = np.kaiser(len(source_sig), 10)
pulse = source_sig*window
pulse_tx = np.concatenate((pulse,np.zeros(int(1e6))))
#samples = np.repeat(pulse, 32) # 16 samples per symbol (rectangular pulses)
pulse_tx *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

sdr.tx(pulse_tx) # start transmitting

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

#waterfall2(RX, 256)
#waterfall(pulse, 256)

#plt.figure()
#plt.plot(t[:slice_len],10*np.log10(abs(DPC[:slice_len])))


plt.ion()
plt.show()