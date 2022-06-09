#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:09:52 2020
Here I plot the evolution of the wave climate
@author: koealaquillage
"""

#*****Import of libraries*********#
import scipy.io as sio
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from scipy.ndimage import gaussian_filter1d
#*****The general variables*******#
data_struc = [] # Empty, to store the data
data_loc = 'OLZO2016_Cris.mat' 

#**** The lists***************#

# Only the stations with eta
stations = ['CP2', 'CP3', 'CP4', 'CP5', 'CP6', 'CP7', 'CP8']
# Now we use a dictionnary to access the significative height
data_dic = {'CP2' : ['timewave','hs_sw'],
            'CP3' : ['timewave','hs_sw'],
            'CP4' : ['timewave','hs_sw'],
            'CP5' : ['timewave','hs_sw'],
            'CP6' : ['timewave','hs_sw'],
            'CP7' : ['timewave','hs_sw'],
            'CP8' : ['timewave','hs_sw']}


#*****Plotting variables******#
fig_eta = plt.figure()
ax_eta = fig_eta.add_subplot()

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
    t,e = data_dic[stat]  # t for time, w for wave
    # 2 the wave data
    time = data_struc['OLZO2016_Cris'][0][0][stat][t][0][0][0,:]
    # And we convert it
#    time = dates.num2date(time)
    eta = data_struc['OLZO2016_Cris'][0][0][stat][e][0][0][0,:]
    # I want to try and smooth it
    eta = gaussian_filter1d(eta,sigma =10)
    # And we plot
    ax_eta.plot(time, eta, label=stat)

ax_eta.legend(loc='best')
ax_eta.set_ylabel('Significative swell wave height (m)')
ax_eta.set_xlabel('Time (days)')