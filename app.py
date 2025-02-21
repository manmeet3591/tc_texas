import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Load the dataset from your GitHub repository
GITHUB_CSV_URL = "https://raw.githubusercontent.com/manmeet3591/tc_texas/main/tc_mask_texas.csv"
df = pd.read_csv(GITHUB_CSV_URL, parse_dates=['time'])

# Load Texas counties shapefile (Upload a valid GeoJSON file in your repo)
TEXAS_GEOJSON_URL = "https://raw.githubusercontent.com/manmeet3591/tc_texas/main/texas_counties.geojson"
gdf = gpd.read_file(TEXAS_GEOJSON_URL)

# Streamlit UI
st.title("Texas TC Mask Visualization")
st.sidebar.header("Filters")

# Year selection
years = sorted(df['time'].dt.year.unique())
selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)

# Scenario selection
scenarios = df['scenario'].unique().tolist()
selected_scenario = st.sidebar.radio("Select Scenario", scenarios)

# Filter data
df_filtered = df[(df['time'].dt.year == selected_year) & (df['scenario'] == selected_scenario)]

# Merge with GeoDataFrame (Ensure county identifiers match between files)
merged = gdf.merge(df_filtered, how='left', left_on='county_column', right_on='lat_lon_column')

# Create Folium map
m = folium.Map(location=[31.9686, -99.9018], zoom_start=6)

folium.Choropleth(
    geo_data=gdf,
    name="choropleth",
    data=merged,
    columns=["county_column", "tc_mask"],
    key_on="feature.properties.county_column",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="TC Mask Values"
).add_to(m)

# Add hover feature
def style_function(feature):
    return {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }

def highlight_function(feature):
    return {
        'fillColor': 'green',
        'color': 'yellow',
        'weight': 3,
        'fillOpacity': 0.7
    }

folium.GeoJson(
    gdf,
    style_function=style_function,
    highlight_function=highlight_function,
    tooltip=folium.GeoJsonTooltip(fields=["county_column", "tc_mask"], aliases=["County", "TC Mask Value"])
).add_to(m)

# Display map in Streamlit
folium_static(m)
