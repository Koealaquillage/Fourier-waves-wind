#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:56:59 2020
Here is a script to import wind data and read them
@author: koealaquillage
"""

#****Packages import********#
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d
#***Now the variables***#
data_loc = 'Vent/Data_wind_Tontouta_Noumea.txt'
wind_data = []

#****Now we import it with pandas****#
wind_data = pd.read_csv(data_loc,skiprows=10,usecols=[3,4,8,11,13,15])
# Now we have to rename some parts of the dataframe
wind_data.rename(columns = {'20160301' : 'Date',
                            '0300':'Time',
                            '180' : 'Wind direction',
                           '  5.7' : 'Wind velocity',
                           '  33.0' : 'Air temperature',
                           '1011.7' : 'Atmospheric Pressure'}, inplace = True)

#****Now I want to fill the missing data
wind_data.replace({999: np.nan}, inplace=True)
wind_data.replace({999.9: np.nan}, inplace=True)
wind_data.replace({9999.9: np.nan}, inplace=True)

#***Now if I interpolate*********#
wind_data['Wind direction'].interpolate(inplace=True)
wind_data['Air temperature'].interpolate(inplace=True)
wind_data['Atmospheric Pressure'].interpolate(inplace=True)

# And now I declare the plots#
fig, axs = plt.subplots()

wind_data['Wind direction'].plot()
wind_data['Air temperature'].plot()
wind_data['Wind velocity'].plot()

# And I declare another plot
fig, ax_wind = plt.subplots()
# Now Maybe I can take the Fourier transform of those
# We must record the length of wave
len_wind = len(wind_data['Wind velocity'])
# But now, we have to Fourier transform those
# But first we need a nice window
w = np.blackman(len_wind)
fft_wind = np.fft.rfft(wind_data['Wind velocity']*w)
# Now we take the product to be real
fft_wind_2 = fft_wind*fft_wind.conj()
# And we smooth it
#fft_wind_2 = gaussian_filter1d(fft_wind_2.real,sigma =3)
# And for the frequency
freq = np.fft.rfftfreq(len_wind, d= 1./48)
# And we plot
ax_wind.semilogy(freq, fft_wind_2)

ax_wind.set_ylabel('Wind speed power ($m^{2}.s^{-2}$)')
ax_wind.set_xlabel('frequency ($days^{-1}$)')

# And for the temperature
# And I declare another plot
fig, ax_air_temp = plt.subplots()
# Now Maybe I can take the Fourier transform of those
# We must record the length of wave
len_airtemp = len(wind_data['Air temperature'])
# But now, we have to Fourier transform those
# But first we need a nice window
w = np.blackman(len_airtemp)
fft_airtemp = np.fft.rfft(wind_data['Air temperature']*w)
# Now we take the product to be real
fft_airtemp_2 = fft_airtemp*fft_airtemp.conj()
# And we smooth it
fft_airtemp_2 = gaussian_filter1d(fft_airtemp_2.real,sigma =3)
# And for the frequency
freq = np.fft.rfftfreq(len_airtemp, d= 1./48)
# And we plot
ax_air_temp.semilogy(freq, fft_airtemp_2)

ax_air_temp.set_ylabel('Air temperature power ($\degree C^{2}$)')
ax_air_temp.set_xlabel('frequency ($days^{-1}$)')


# And for the direction, yet another plot

# And for the temperature
# And I declare another plot
fig, ax_wind_dir = plt.subplots()
# Now Maybe I can take the Fourier transform of those
# We must record the length of wave
len_wind_dir = len(wind_data['Wind direction'])
# But now, we have to Fourier transform those
# But first we need a nice window
w = np.blackman(len_wind_dir)
fft_winddir = np.fft.rfft(wind_data['Wind direction']*w)
# Now we take the product to be real
fft_winddir_2 = fft_winddir*fft_winddir.conj()
# And we smooth it
fft_winddir_2 = gaussian_filter1d(fft_winddir_2.real,sigma =3)
# And for the frequency
freq = np.fft.rfftfreq(len_wind_dir, d= 1./48)
# And we plot
ax_wind_dir.semilogy(freq, fft_winddir_2)

ax_wind_dir.set_ylabel('Air temperature power ($\degree^{2}$)')
ax_wind_dir.set_xlabel('frequency ($days^{-1}$)')

# And for the atmospheric pressure #

# And for the temperature
# And I declare another plot
fig, ax_press = plt.subplots()
# Now Maybe I can take the Fourier transform of those
# We must record the length of wave
len_press = len(wind_data['Atmospheric Pressure'][5:])
# But now, we have to Fourier transform those
# But first we need a nice window
w = np.blackman(len_press)
fft_press = np.fft.rfft(wind_data['Atmospheric Pressure'][5:]*w)
# Now we take the product to be real
fft_press_2 = fft_press*fft_press.conj()
# And we smooth it
fft_press_2 = gaussian_filter1d(fft_press_2.real,sigma =3)
# And for the frequency
freq = np.fft.rfftfreq(len_press, d= 1./48)
# And we plot
ax_press.semilogy(freq, fft_press_2)

ax_press.set_ylabel('Pressure power ($millibar^{2}$)')
ax_press.set_xlabel('frequency ($days^{-1}$)')

