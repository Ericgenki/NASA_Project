from satpy import Scene, find_files_and_readers
from pyresample import create_area_def
from satpy.writers import get_enhanced_image
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from celluloid import Camera
from satpy import MultiScene
from satpy.multiscene import timeseries

def figure(storm, region):

    i=0
    base = '/home/hboi-ouri/Projects/RS_Files/' + storm + '/MYD021KM.'

    #files to be used
    filenames = glob('/home/hboi-ouri/Projects/RS_Files/' + storm + '/MYD021KM.*')
    swats = np.unique([f.split('.')[1] for f in filenames])

    #area in the figure
    if(region == "TXLA"):
        extent = [-94, 27.5, -88, 30.5]
        my_area = create_area_def('my_area', {'proj': 'lcc', 'lon_0': -91., 'lat_0': 29.5, 'lat_1': 29.5, 'lat_2': 29.5},
                        width=1500, height=750,
                        area_extent=extent, units='degrees')
    elif(region == "FLBay"):
        extent = [-81.2, 24.9, -80.4, 25.3]
        my_area = create_area_def('my_area', {'proj': 'lcc', 'lon_0': -80.8, 'lat_0': 25.2, 'lat_1': 25.2, 'lat_2': 25.2},
                        width=1500, height=750,
                        area_extent=extent, units='degrees')

    # for animation
    fig =  plt.figure(figsize=(6, 4), dpi=400)
    camera = Camera(fig)

    #creating animation
    for swat in swats:
        dayfiles = glob(base+swat+'*')
        scn = Scene(dayfiles, reader='modis_l1b')
        scn.load(['true_color'])

        #reproject
        new_scn = scn.resample(my_area)

        #generate RGB from true color
        rgb = get_enhanced_image(new_scn['true_color'])

        #extract projection and lon lat from products
        crs = new_scn['true_color'].attrs['area'].to_cartopy_crs()
        lons, lats = new_scn['true_color'].attrs['area'].get_lonlats()

        #set up figure size and resolution

        #left true color
        ax1 = plt.subplot(1, 2, 1, projection=crs)
        rgb.data.plot.imshow(rgb='bands', transform=crs, ax=ax1)
        ax1.set_title('True Color')

        #optimize spacing between plots
        fig.tight_layout()

        #for each frame of animation
        camera.snap()

    #save
    animation = camera.animate(interval=1000)
    animation.save('/home/hboi-ouri/Projects/NASA_Project/outputs/' + storm + 'animation.mp4')
