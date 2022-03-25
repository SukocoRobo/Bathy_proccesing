"""
This is python code for bathymetric data proccessing
"""
import numpy as np
import pandas as pd
from numpy import genfromtxt

data_dir = "/16 Pyhton/1 Python Training/Bathy_proccesing/"
file_name = data_dir + "example_survey_data.csv"
bath_data = genfromtxt(file_name, delimiter=',')

type(bath_data)
print(bath_data.ndim)
print(bath_data.shape)

lat = bath_data[:,0]
lon = bath_data[:,1]
depth = bath_data[:,2]

import matplotlib.pyplot as plt
plt.title("Bathy measurement locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.plot(lon,lat,'.')
dL = 0.0005
plt.xlim([lon.min()-dL, lon.max()+dL])
plt.ylim([lat.min()-dL, lat.max()+dL])
plt.show()

import matplotlib.ticker as mtick

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(lon,lat,'.')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.title("Bathy measurement locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

from matplotlib  import cm
fig = plt.figure() # (figsize=(20,6))
ax = fig.add_subplot(111)
sc = ax.scatter(lon,lat,s = 20,c = depth, marker = 'o', cmap = cm.jet );
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar(sc)
plt.show()

import pyproj as pjo
from pyproj import Proj
myProj = Proj("+proj=utm +zone=49N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_def")
UTMx, UTMy = myProj(lon, lat)
