#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 17:33:28 2020

@author: koealaquillage

# Here we want to have a script to import data#
# of wave from a .mat file #

I have an issue ( 15/04/2020) with the timestamp conversion,
but it is likely due to my version of python. So I'll see when I update
"""

#*****Import of libraries*********#
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.dates as dates

#*****The general variables*******#
data_struc = [] # Empty, to store the data
data_loc = 'OLZO2016_Cris.mat' 

#**** The lists***************#

stations = ['Offshore','S4','CP2','CP3','CP4','CP5','CP6','CP7','CP8']
# Only the stations with eta
stations_eta = ['CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CP7', 'CP8']
# Now we use a dictionnary to access the significative height
data_dic = {'Offshore' : ['time','hs'],
            'S4' : ['time','hs'],
            'CP2' : ['timewave','hs_sw'],
            'CP3' : ['timewave','hs_sw'],
            'CP4' : ['timewave','hs_sw'],
            'CP5' : ['timewave','hs_sw'],
            'CP6' : ['timewave','hs_sw'],
            'CP7' : ['timewave','hs_sw'],
            'CP8' : ['timewave','hs_sw']}


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
    # And we convert it
#    time = dates.num2date(time)
    wave = data_struc['OLZO2016_Cris'][0][0][stat][w][0][0][0,:]
    # And we plot
    ax_wave.plot(time, wave, label=stat)

ax_wave.legend(loc='best')
ax_wave.set_ylabel('Wave height (m)')
ax_wave.set_xlabel('Time (days)')