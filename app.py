import streamlit as st
import xarray as xr
import geopandas as gpd
import folium
from folium.plugins import MousePosition
from branca.colormap import linear
import numpy as np
import os

# Title
st.title("Texas Tropical Cyclone Mask Analysis")

# User input for Year
year = st.selectbox("Select a Year:", list(range(1979, 2101)), index=0)

# Scenario selection based on the year
if year < 2015:
    scenario = "historical"
else:
    scenario = st.selectbox("Select a Scenario:", ["ssp245", "ssp585"])

# Construct file path
file_path = f"data/tc_texas_{scenario}_{year}.nc"

# Load Texas County Boundaries
@st.cache_data
def load_texas_counties():
    counties = gpd.read_file("https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json")
    texas_counties = counties[counties["STATE"] == "48"]  # Texas state FIPS code
    return texas_counties

texas_counties = load_texas_counties()

# Load NetCDF file
@st.cache_data
def load_netcdf(file_path):
    if os.path.exists(file_path):
        ds = xr.open_dataset(file_path)
        return ds
    else:
        st.error(f"File {file_path} not found!")
        return None

ds = load_netcdf(file_path)

# Process and map the data
if ds:
    st.write(f"Loaded NetCDF file: {file_path}")
    
    # Extract tc_mask and convert to Pandas DataFrame
    latitudes = ds.lat.values
    longitudes = ds.lon.values
    tc_mask = ds.tc_mask.values if "tc_mask" in ds else None  # Extract tc_mask variable

    if tc_mask is not None:
        # Create a DataFrame for mapping
        lons, lats = np.meshgrid(longitudes, latitudes)
        data = {"Longitude": lons.flatten(), "Latitude": lats.flatten(), "TC_Mask": tc_mask.flatten()}

        # Convert tc_mask into a county-level sum
        texas_counties["TC_Mask_Sum"] = 0  # Initialize column

        # for index, county in texas_counties.iterrows():
        #     mask = (
        #         (data["Longitude"] >= county.bounds[0]) & (data["Longitude"] <= county.bounds[2]) &
        #         (data["Latitude"] >= county.bounds[1]) & (data["Latitude"] <= county.bounds[3])
        #     )
        #     texas_counties.at[index, "TC_Mask_Sum"] = np.sum(np.array(data["TC_Mask"])[mask])
        for index, county in texas_counties.iterrows():
            minx, miny, maxx, maxy = county.geometry.bounds  # Extract bounds properly
        
            # Create a Boolean mask
            mask = (
                (data["Longitude"] >= minx) & (data["Longitude"] <= maxx) &
                (data["Latitude"] >= miny) & (data["Latitude"] <= maxy)
            )
        
            # Ensure that the mask is not empty before applying it
            masked_values = np.array(data["TC_Mask"])[mask]
        
            if masked_values.size > 0:  # Avoid indexing empty array
                texas_counties.at[index, "TC_Mask_Sum"] = np.sum(masked_values)
            else:
                texas_counties.at[index, "TC_Mask_Sum"] = 0  # Assign zero if no data found

        # for index, county in texas_counties.iterrows():
        #     minx, miny, maxx, maxy = county.geometry.bounds  # Extract bounds properly
        #     mask = (
        #         (data["Longitude"] >= minx) & (data["Longitude"] <= maxx) &
        #         (data["Latitude"] >= miny) & (data["Latitude"] <= maxy)
        #             )
        #     texas_counties.at[index, "TC_Mask_Sum"] = np.sum(np.array(data["TC_Mask"])[mask])

        # Create a map
        m = folium.Map(location=[31, -99], zoom_start=5)

        # Color map based on tc_mask sum
        colormap = linear.YlOrRd_09.scale(
            texas_counties["TC_Mask_Sum"].min(), texas_counties["TC_Mask_Sum"].max()
        )

        # Add Texas counties with tooltips
        for _, row in texas_counties.iterrows():
            folium.GeoJson(
                row.geometry,
                style_function=lambda feature: {
                    "fillColor": colormap(row["TC_Mask_Sum"]),
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.6,
                },
                tooltip=folium.Tooltip(
                    f"County: {row['NAME']}<br>TC Mask Sum: {row['TC_Mask_Sum']}"
                ),
            ).add_to(m)

        # Add hover functionality
        MousePosition().add_to(m)

        # Show the map in Streamlit
        st.write("## Texas Counties Affected by Tropical Cyclones")
        st.write("Hover over a county to see the TC Mask Sum.")

        folium_static(m)

    else:
        st.error("NetCDF file does not contain 'tc_mask' variable.")
