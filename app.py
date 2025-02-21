import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Load the dataset from your GitHub repository
GITHUB_CSV_URL = "https://raw.githubusercontent.com/manmeet3591/tc_texas/main/tc_mask_texas.csv"
df = pd.read_csv(GITHUB_CSV_URL, parse_dates=['time'])

# Load the Texas counties GeoJSON file from your repository
GEOJSON_PATH = "Texas_County_Boundaries_-2028607862104916578.geojson"  # Ensure this path matches the location in your repo
gdf = gpd.read_file(GEOJSON_PATH)

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

# Ensure the 'county_column' in gdf matches with a column in df_filtered
# You might need to perform spatial joins or have a common key for merging
# For example, if both have a 'county_name' column:
# merged = gdf.merge(df_filtered, how='left', left_on='county_name', right_on='county_name')

# Create Folium map
m = folium.Map(location=[31.9686, -99.9018], zoom_start=6)

# Add Choropleth layer
folium.Choropleth(
    geo_data=gdf,
    name="choropleth",
    data=df_filtered,
    columns=["county_name", "tc_mask"],  # Ensure these columns exist
    key_on="feature.properties.county_name",  # Match this with the GeoJSON properties
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="TC Mask Values"
).add_to(m)

# Add hover functionality
folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    },
    highlight_function=lambda feature: {
        'fillColor': 'green',
        'color': 'yellow',
        'weight': 3,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["county_name"],  # Adjust based on your GeoJSON properties
        aliases=["County: "]
    )
).add_to(m)

# Display map in Streamlit
folium_static(m)
