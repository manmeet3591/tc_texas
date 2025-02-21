# import streamlit as st
# import pandas as pd
# import numpy as np

# # Load the dataset
# @st.cache_data
# def load_data():
#     df = pd.read_csv("tc_texas_counties.csv")
#     return df

# data = load_data()

# # Convert data types to avoid errors
# data["Year"] = pd.to_numeric(data["Year"], errors='coerce')
# data["TC"] = pd.to_numeric(data["TC"], errors='coerce')

# data.dropna(inplace=True)  # Remove invalid entries

# # Ensure Scenario and County columns are string to avoid errors
# data["Scenario"] = data["Scenario"].astype(str)
# data["County"] = data["County"].astype(str)

# # Streamlit App Layout
# st.title("Texas Tropical Cyclones Past and Future Scenarios")

# # Sidebar Filters
# years = sorted(data["Year"].unique())
# scenarios = sorted(data["Scenario"].unique())
# counties = sorted(data["County"].unique())

# selected_year = st.sidebar.selectbox("Select Year", years)
# selected_scenario = st.sidebar.selectbox("Select Scenario", scenarios)
# selected_county = st.sidebar.selectbox("Select County", counties)

# # Filter data based on selections
# filtered_data = data[(data["Year"] == selected_year) & (data["Scenario"] == selected_scenario) & (data["County"] == selected_county)]

# # Drop the first column before displaying
# filtered_data = filtered_data.iloc[:, 1:]

# # Display results
# st.write(f"### Number of Tropical Cyclones for {selected_county} in {selected_scenario} scenario in {selected_year}")
# st.dataframe(filtered_data.rename(columns={"TC": "Tropical Cyclones"}), hide_index=True)



#######################################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the datasets
@st.cache_data
def load_data():
    df_tc = pd.read_csv("tc_texas_counties.csv")
    df_coords = pd.read_csv("texas_counties.csv")
    return df_tc, df_coords

data, county_coords = load_data()

# Convert data types to avoid errors
data["Year"] = pd.to_numeric(data["Year"], errors='coerce')
data["TC"] = pd.to_numeric(data["TC"], errors='coerce')

data.dropna(inplace=True)  # Remove invalid entries

# Ensure Scenario and County columns are string to avoid errors
data["Scenario"] = data["Scenario"].astype(str)
data["County"] = data["County"].astype(str)
county_coords["COUNTY"] = county_coords["COUNTY"].astype(str)

# Streamlit App Layout
st.title("Texas Tropical Cyclones Data Viewer")

# Sidebar Filters
years = sorted(data["Year"].unique())
scenarios = sorted(data["Scenario"].unique())

selected_year = st.sidebar.selectbox("Select Year", years)
selected_scenario = st.sidebar.selectbox("Select Scenario", scenarios)

# Filter data based on selections
filtered_data = data[(data["Year"] == selected_year) & (data["Scenario"] == selected_scenario)]

# Merge with county coordinates
merged_data = filtered_data.merge(county_coords, left_on="County", right_on="COUNTY", how="left")

# Plot map
tx_fig = px.scatter_mapbox(
    merged_data,
    lat="lat",
    lon="lon",
    size="TC",
    hover_name="County",
    hover_data={"lat": False, "lon": False, "TC": True},
    color_continuous_scale="Viridis",
    size_max=15,
    zoom=5,
    mapbox_style="carto-positron",
)

st.write(f"### Tropical Cyclones across Texas for {selected_scenario} scenario in {selected_year}")
st.plotly_chart(tx_fig)
