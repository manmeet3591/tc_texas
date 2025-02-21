import xarray as xr

ds_tc_ssp585 = xr.open_mfdataset('tc/tc_ssp585_????.nc').compute()
print(ds_tc_ssp585)