# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 21:09:23 2021
I wish this could be a .ipy file so I could set matplotlib graphing options
@author: Zac
"""

import matplotlib.pyplot as plt
import numpy as np
from pint import UnitRegistry # u for unit

#%matplotlib qt
#%matplotlib inline

def distance(t, unit):
    # altitude = # todo: look into if air density measurably affects range
    # temp = 20 # degrees C
    # c = some equation relating density
    units = ('km','mi','nmi','m','yd',)
    if not unit in units:
        raise Exception("invalid distance unit conversion input")
    return()

def waterfall(iq,n=1024,fs=1e6):
    global freq_domain
    freq_domain = np.zeros((int(len(iq)/n),n))
    for i in range(int((len(iq)-n)/n)):
        try:
            freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        except Exception:
            print('error')
    print("FFT shape", freq_domain.shape)
    # freq_domain = np.roll(freq_domain,int(n/2)) # center frequency at 0
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,1,1,0],interpolation='nearest')


def waterfall2(iq,n=1024,fs=1e6,dec=10):
    global freq_domain
    #freq_domain = np.zeros((int(len(iq)),n))
    freq_domain = np.zeros(n)
    print(int(len(iq)))
    for i in range(int(len(iq)/dec)):
        #print((i+1)*n-i*n)
        #freq_domain[i] = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        #temp = 10*np.log10(abs(np.fft.fft(iq[i*n:(i+1)*n],n)**2))
        temp = 10*np.log10(abs(np.fft.fft(iq[(i*dec):(i*dec)+1+n],n)**2))
        #print(temp)
        freq_domain = np.vstack((freq_domain,temp))
        #if i > 5:
            #break
         #   continue
    print("FFT shape",freq_domain.shape)
    freq_domain = np.roll(freq_domain,int(n/2)) # center frequency at 0
    plt.figure()
    plt.imshow(freq_domain, cmap='hot')#, extent=[-fs/1e6,fs/1e6,len(freq_domain),0])#interpolation='nearest')
    #plt.plot(freq_domain[5])

def waterfall3(iq,n=1024,fs=1e6,padz=512):
    global freq_domain
    freq_domain = np.zeros((int(len(iq)/n),n))
    for i in range(int((len(iq)-n)/n)):
        try:
            # Not sure the zero padding does anything useful yet.
            # Also graphing has a problem at the start and end.
            # Probably because of the roll function.
            tmp = iq[i*n:(i+1)*n]
            np.pad(tmp, (padz, padz), 'constant', constant_values=(0, 0))
            freq_domain[i] = 10*np.log10(abs(np.fft.fft(tmp,n)**2))
        except Exception:
            print('error')
    print("FFT shape", freq_domain.shape)
    freq_domain = np.roll(freq_domain,int(n/2)) # center frequency at 0
    plt.figure()
    plt.imshow(freq_domain, cmap='hot', extent=[0,1,1,0],interpolation='nearest')


def plot_iq(iq):
    plt.figure()
    plt.plot(iq.real)
    plt.plot(iq.imag)

