import numpy as np
import datetime
import zipfile
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


def grid_bathy(file_name, ucols):
    # lat = column 0, lon = column 1, depth = column 2
    bath_data = np.loadtxt(file_name, delimiter=',', usecols=ucols)
    lon_grid, lat_grid = np.meshgrid(np.linspace(bath_data[:, 1].min(), bath_data[:, 1].max(), 40),
                                     np.linspace(bath_data[:, 0].min(), bath_data[:, 0].max(), 40), sparse=False,
                                     indexing='xy')
    z_grid = griddata((bath_data[:, 1], bath_data[:, 0]), bath_data[:, 2], (lon_grid, lat_grid), method='cubic')
    return lon_grid, lat_grid, z_grid


data_dir = "/16 Pyhton/1 Python Training/Bathy_proccesing/"
file_name = data_dir + "example_survey_data.csv"
ucols = (0, 1, 2)
lon_grid, lat_grid, z_grid = grid_bathy(file_name, ucols)

from simplekml import (Kml, OverlayXY, ScreenXY, Units, RotationXY,
                       AltitudeMode, Camera)


def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):
    kml = Kml()
    altitude = kw.pop('altitude', 2e3)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=np.mean([urcrnrlat, llcrnrlat]),
                    longitude=np.mean([urcrnrlon, llcrnrlon]),
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', 'overlay')
        ground.color = kw.pop('color', '9effffff')
        ground.atomauthor = kw.pop('author', 'squirm_tech')
        ground.latlonbox.rotation = kw.pop('rotation', 0)
        ground.description = kw.pop('description', 'Matplotlib figure')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToSeaFloor')
        ground.icon.href = fig
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.015, y=0.075,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    kmzfile = kw.pop('kmzfile', 'overlay.kmz')
    kml.savekmz(kmzfile)

def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi/180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.
    fig = plt.figure(figsize=figsize,
                     frameon=False,
                     dpi=pixels//10)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    return fig, ax

pixels = 1024 * 10
from matplotlib  import cm
cmap = cm.jet
fig, ax = gearth_fig(llcrnrlon=lon_grid.min(),
                     llcrnrlat=lat_grid.min(),
                     urcrnrlon=lon_grid.max(),
                     urcrnrlat=lat_grid.max(),
                     pixels=pixels)
cs = ax.pcolormesh(lon_grid, lat_grid, z_grid, cmap=cmap, shading='auto')
ax.set_axis_off()
fig.savefig('overlay1.png', transparent=False, format='png')
fig = plt.figure(figsize=(1.0, 4.0), facecolor='None', frameon=False)
ax = fig.add_axes([0.0, 0.05, 0.2, 0.9])
cb = fig.colorbar(cs, cax=ax)
cb.set_label('Depth [m]', rotation=-90, color='w', labelpad=20)
cb.ax.yaxis.set_tick_params(color='w')
plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='w')
fig.savefig('legend.png', transparent=False, format='png')

make_kml(llcrnrlon=lon_grid.min(), llcrnrlat=lat_grid.min(),
         urcrnrlon=lon_grid.max(), urcrnrlat=lat_grid.max(),
         figs=['overlay1.png'], colorbar='legend.png',
         kmzfile='bathy_colorbar.kmz', name='Depth [m]')

