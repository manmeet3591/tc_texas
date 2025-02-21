import streamlit as st
import pandas as pd
import numpy as np

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("tc_texas_counties.csv")
    return df

data = load_data()

# Convert data types to avoid errors
data["Year"] = pd.to_numeric(data["Year"], errors='coerce')
data["TC"] = pd.to_numeric(data["TC"], errors='coerce')

data.dropna(inplace=True)  # Remove invalid entries

# Ensure Scenario and County columns are string to avoid errors
data["Scenario"] = data["Scenario"].astype(str)
data["County"] = data["County"].astype(str)

# Streamlit App Layout
st.title("Texas Tropical Cyclones Past and Future Scenarios")

# Sidebar Filters
years = sorted(data["Year"].unique())
scenarios = sorted(data["Scenario"].unique())
counties = sorted(data["County"].unique())

selected_year = st.sidebar.selectbox("Select Year", years)
selected_scenario = st.sidebar.selectbox("Select Scenario", scenarios)
selected_county = st.sidebar.selectbox("Select County", counties)

# Filter data based on selections
filtered_data = data[(data["Year"] == selected_year) & (data["Scenario"] == selected_scenario) & (data["County"] == selected_county)]

# Drop the first column before displaying
filtered_data = filtered_data.iloc[:, 1:]

# Display results
st.write(f"### Number of Tropical Cyclones for {selected_county} in {selected_scenario} scenario in {selected_year}")
st.dataframe(filtered_data.rename(columns={"TC": "Tropical Cyclones"}), hide_index=True)
