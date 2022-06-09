#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 11:47:00 2020

Here we plot the external Fourier transform of the wave signal 
for the Offshore and the S4 station
@author: koealaquillage
"""

#*****Import of libraries*********#
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np

#*****The general variables*******#
data_struc = [] # Empty, to store the data
data_loc = 'OLZO2016_Cris.mat' 

#**** The lists***************#

stations = ['Offshore','S4']
# Now we use a dictionnary to access the significative height
data_dic = {'Offshore' : ['time','hs'],
            'S4' : ['time','hs']}


#*****Plotting variables******#
fig_wave = plt.figure()
ax_wave = fig_wave.add_subplot()

#****Now we do the import******#
data_struc = sio.loadmat(data_loc)

#******Little explanation*******#
""" 
The data structure is a rather complicated one,
as it is inherited from a matlab matrix file.
Therefore, the data in themselves are accessed by
data_struc['OLZO2016_Cris'][0][0], the upper levels
being used for metadata about the file.

Once there, the general structure is a dictionnary. 
The different keys of the dictionnary are the different 
stations in New-Caledonia at that time and are :
Offshore, S4, CP2, CP3, CP4, CP5, CP6, CP7 and CP8

I do not really know the position of those stations. But,
I know what data they might contain. Most of them contain only wave data, 
however, some also include low frequency overelevation informations. The
entire set of data is :

timewave, hs_sw, hs_ig, hs_vlf, timeeta, eta (CP2, CP3, CP4, CP5, CP6,
 CP7 and CP8)

or

time, hs, tp, dir (Offshore)

or 

time, hs, ho, tp, dir (S4)

And to access those, I must use the total path : 
data_struc['OLZO2016_Cris'][0][0]['S4']['timewave'][0][0][0,:]

for example
"""

#***** Ok, now we can plot*******#

for stat in stations :
    # Now we import the data in temporary variables
    t,w = data_dic[stat]  # t for time, w for wave
    # 2 the wave data
    time = data_struc['OLZO2016_Cris'][0][0][stat][t][0][0][0,:]
    # Now we have to save the sampling of this time structure
    # Note that the unit of time recording is day, so the output frequency
    # Will be in day -1
    t_samp = np.mean(time[1:]-time[:-1])
    # And we convert it
#    time = dates.num2date(time)
    wave = data_struc['OLZO2016_Cris'][0][0][stat][w][0][0][0,:]
    # Now we do the padding
    time = time[56:]
    wave = wave[56:]
    # We must record the length of wave
    len_wave = len(wave)
    # But now, we have to Fourier transform those
    # But first we need a nice window
    w = np.blackman(len_wave)
    fft_wave = np.fft.rfft(wave*w)
    # Now we take the product to be real
    fft_wave_2 = fft_wave*fft_wave.conj()
    # And for the frequency
    freq = np.fft.rfftfreq(len_wave, d= t_samp)
    # And we plot
    ax_wave.semilogy(freq, fft_wave_2, label=stat)

ax_wave.legend(loc='best')
ax_wave.set_ylabel('Wave power (m^2)')
ax_wave.set_xlabel('frequency (days^-1)')

