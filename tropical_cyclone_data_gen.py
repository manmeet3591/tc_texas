# import xarray as xr
# import numpy as np
# import xarray as xr

# import scipy.ndimage #import gaussian_filter
# import metpy.calc as mpcalc
# from metpy.units import units

# import sys

# scenario = 'ssp585'
# year = '2050'

# filepath = '/media/ms86336/SSD 2/backup_ssd2/shweta/ua_day/ua_day_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gr_20500101-20501231.nc'
# ds_ua_ssp585 = xr.open_mfdataset(filepath)
# filepath = '/media/ms86336/SSD 2/backup_ssd2/shweta/va_day/va_day_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gr_20500101-20501231.nc'
# ds_va_ssp585 = xr.open_mfdataset(filepath)
# filepath = '/media/ms86336/SSD 2/backup_ssd2/shweta/hus_day/hus_day_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gr_20500101-20501231.nc'
# ds_hus_ssp585 = xr.open_mfdataset(filepath)
# ds_tas_ssp585 = xr.open_mfdataset('/media/ms86336/SSD 2/backup_ssd2/shweta/tas_day/tas_day_EC-Earth3-Veg-LR_ssp585_r1i1p1f1_gr_20500101-20501231.nc')

# import metpy.calc as mpcalc

# # Calculate the vertical vorticity of the flow
# # 🔹 Extract Relevant Variables
# ua_850 = ds_ua_ssp585['ua'].sel(plev=85000)  # 850 hPa zonal wind (m/s)
# va_850 = ds_va_ssp585['va'].sel(plev=85000)  # 850 hPa meridional wind (m/s)
# vort = mpcalc.vorticity(ua_850, va_850)

# # Calculate the stretching deformation of the flow
# str_def = mpcalc.stretching_deformation(ua_850, va_850)

# # Calculate the shearing deformation of the flow
# shr_def = mpcalc.shearing_deformation(ua_850, va_850)

# # Compute Okubo-Weiss-Zeta parameter (OWZP)
# zeta = vort
# stretching = str_def
# shearing = shr_def
# ow_norm = (zeta**2 - (stretching**2 + shearing**2)) / (zeta**2)
# owzp = np.maximum(ow_norm, 0) * zeta

# # Apply Gaussian smoothing to filter small-scale noise
# owzp = scipy.ndimage.gaussian_filter(owzp, sigma=1.5)

# vort['owzp'] = (('time', 'lat', 'lon'), owzp)

# # Threshold for TC detection (adjust based on model resolution)
# TC_THRESHOLD = 1e-5  # Example value, refine as needed
# tc_mask = owzp > TC_THRESHOLD

# vort['tc_mask'] = (('time', 'lat', 'lon'), tc_mask)

# vort.to_dataset().compute().to_netcdf('tc_'+scenario+'_'+year+'.nc')

import xarray as xr
import numpy as np
import scipy.ndimage
import metpy.calc as mpcalc
from metpy.units import units
from tqdm import tqdm  # Progress bar

# # Define scenarios and years
# scenarios = ['ssp585', 'ssp245']
# years = range(2015, 2101)  # From 2015 to 2100
# Define scenarios and years
scenarios = ['historical']
years = range(1979, 2015)  # From 2015 to 2100
# Base directory for data files (adjust path as needed)
base_dir = '/media/ms86336/SSD 2/backup_ssd2/shweta/'

# Threshold for tropical cyclone detection (adjust as needed)
TC_THRESHOLD = 1e-5  

# Loop over scenarios and years with tqdm progress bar
for scenario in tqdm(scenarios, desc="Processing Scenarios"):
    for year in tqdm(years, desc=f"Processing Years for {scenario}", leave=False):
        try:
            # Construct file paths dynamically
            filepath_ua = f'{base_dir}ua_day/ua_day_EC-Earth3-Veg-LR_{scenario}_r1i1p1f1_gr_{year}0101-{year}1231.nc'
            filepath_va = f'{base_dir}va_day/va_day_EC-Earth3-Veg-LR_{scenario}_r1i1p1f1_gr_{year}0101-{year}1231.nc'
            # filepath_hus = f'{base_dir}hus_day/hus_day_EC-Earth3-Veg-LR_{scenario}_r1i1p1f1_gr_{year}0101-{year}1231.nc'
            # filepath_tas = f'{base_dir}tas_day/tas_day_EC-Earth3-Veg-LR_{scenario}_r1i1p1f1_gr_{year}0101-{year}1231.nc'
            #print(filepath_ua)
            # Open datasets
            ds_ua = xr.open_mfdataset(filepath_ua)
            ds_va = xr.open_mfdataset(filepath_va)
            # ds_hus = xr.open_mfdataset(filepath_hus)
            # ds_tas = xr.open_mfdataset(filepath_tas)

            # Extract 850 hPa wind components
            ua_850 = ds_ua['ua'].sel(plev=85000)  # 850 hPa zonal wind
            va_850 = ds_va['va'].sel(plev=85000)  # 850 hPa meridional wind

            # Compute vorticity, stretching, and shearing deformation
            vort = mpcalc.vorticity(ua_850, va_850)
            str_def = mpcalc.stretching_deformation(ua_850, va_850)
            shr_def = mpcalc.shearing_deformation(ua_850, va_850)

            # Compute Okubo-Weiss-Zeta parameter (OWZP)
            ow_norm = (vort**2 - (str_def**2 + shr_def**2)) / (vort**2)
            owzp = np.maximum(ow_norm, 0) * vort

            # Apply Gaussian smoothing
            owzp = scipy.ndimage.gaussian_filter(owzp, sigma=1.5)

            # Store results in dataset
            vort_ds = vort.to_dataset()
            vort_ds['owzp'] = (('time', 'lat', 'lon'), owzp)

            # Create tropical cyclone mask
            tc_mask = owzp > TC_THRESHOLD
            vort_ds['tc_mask'] = (('time', 'lat', 'lon'), tc_mask)

            # Save to NetCDF
            output_file = f'tc_{scenario}_{year}.nc'
            vort_ds.compute().to_netcdf(output_file)

        except Exception as e:
            print(f"❌ Error processing {scenario} {year}: {e}")
