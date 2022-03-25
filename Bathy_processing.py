"""
This is python code for bathymetric data processing
"""
import numpy as np
from numpy import genfromtxt
from pyproj import Proj
from scipy.interpolate import griddata
from matplotlib import cm
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

data_dir = "/16 Pyhton/1 Python Training/Bathy_proccesing/"
file_name = data_dir + "example_survey_data.csv"
bath_data = genfromtxt(file_name, delimiter=',')

type(bath_data)
print(bath_data.ndim)
print(bath_data.shape)

lat = bath_data[:, 0]
lon = bath_data[:, 1]
depth = bath_data[:, 2]

plt.title("Bathy measurement locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.plot(lon, lat, '.')
dL = 0.0005
plt.xlim([lon.min() - dL, lon.max() + dL])
plt.ylim([lat.min() - dL, lat.max() + dL])
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(lon, lat, '.')
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.title("Bathy measurement locations")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

fig = plt.figure()  # (figsize=(20,6))
ax = fig.add_subplot(111)
sc = ax.scatter(lon, lat, s=20, c=depth, marker='o', cmap=cm.jet)
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar(sc)
plt.show()

myProj = Proj(proj='utm', zone=49, ellps='WGS84', preserve_units=False)
# Proj('+proj=utm +zone=49N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs', preserve_units=False)
UTMx, UTMy = myProj(lon, lat)
UTMx.max() - UTMx.min()
UTMy.max() - UTMy.min()

dX = 10
X = np.arange(UTMx.min(), UTMx.max(), dX)
Y = np.arange(UTMy.min(), UTMy.max(), dX)
grid_x, grid_y = np.meshgrid(X, Y, sparse=False, indexing='xy')

zi = griddata((UTMx, UTMy), depth, (grid_x, grid_y), method='linear')

print(grid_x.shape)
print(zi.shape)

# fig = plt.figure(figsize=(20,6))
fig = plt.figure()
ax = fig.add_subplot(111)
cp = plt.contourf(grid_x, grid_y, zi)
plt.show()

lon_spc = np.linspace(lon.min(), lon.max(), 40)
lat_spc = np.linspace(lat.min(), lat.max(), 40)
lon_grid, lat_grid = np.meshgrid(lon_spc, lat_spc, sparse=False, indexing='xy')
zL = griddata((lon, lat), depth, (lon_grid, lat_grid), method='cubic')
# fig = plt.figure(figsize=(30, 6))
fig = plt.figure()
ax = fig.add_subplot(111)
cp = plt.contourf(lon_grid, lat_grid, zL, cmap=cm.jet)
ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.4f'))
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.colorbar(cp)
plt.show()
