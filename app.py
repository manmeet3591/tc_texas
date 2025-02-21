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

# data.dropna(inplace=True)  # Remove invalid entries

# # Ensure Scenario column is string to avoid boolean-related errors
# data["Scenario"] = data["Scenario"].astype(str)

# # Streamlit App Layout
# st.title("Texas Tropical Cyclones Data Viewer")

# # Sidebar Filters
# years = sorted(data["Year"].unique())
# scenarios = sorted(data["Scenario"].unique())

# selected_year = st.sidebar.selectbox("Select Year", years)
# selected_scenario = st.sidebar.selectbox("Select Scenario", scenarios)

# # Filter data based on selections
# filtered_data = data[(data["Year"] == selected_year) & (data["Scenario"] == selected_scenario)]

# # Display results
# st.write(f"### Number of Tropical Cyclones for {selected_scenario} scenario in {selected_year}")
# st.dataframe(filtered_data.rename(columns={"TC": "Tropical Cyclones"}), hide_index=True)
