from satpy import Scene, find_files_and_readers
from pyresample import create_area_def
from satpy.writers import get_enhanced_image
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from satpy import MultiScene

    
i=0
base = '/home/hboi-ouri/Projects/RS_Files/TXLADailies/DailyImage/MYD021KM.'

#files to be used
filenames = glob('/home/hboi-ouri/Projects/RS_Files/TXLADailies/DailyImage/MYD021KM.*')
swats = np.unique([f.split('.')[1] for f in filenames])
    
#area in the figure
extent = [-94, 27.5, -88, 30.5]
my_area = create_area_def('my_area', {'proj': 'lcc', 'lon_0': -91., 'lat_0': 29.5, 'lat_1': 29.5, 'lat_2': 29.5},
            width=1500, height=750,
            area_extent=extent, units='degrees')    
        
fig =  plt.figure(figsize=(6, 4), dpi=400)

#loop
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

    #true color
    ax1 = plt.subplot(projection=crs)
    rgb.data.plot.imshow(rgb='bands', transform=crs, ax=ax1)
        
    #title & save
    ax1.set_title('MODISA_Mdelta_%s' % new_scn.start_time.isoformat())
    fig.savefig('/home/hboi-ouri/Projects/NASA_Project/outputs/DailyImages/TXLA/MODISA_Mdelta_%s_rgb.png' % new_scn.start_time.isoformat())