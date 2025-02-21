import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import os

# Streamlit App Title
st.title("Texas Climate Data Viewer")

# User selects scenario
scenario = st.selectbox("Select Scenario:", ["historical", "ssp245", "ssp585"])

# User selects year
if scenario == "historical":
    years = list(range(1979, 2015))  # Historical years
else:
    years = list(range(2015, 2101))  # Future projections

year = st.selectbox("Select Year:", years)

# File path pattern
file_path = f"data/tc_texas_{scenario}_{year}.nc"

# Load and visualize data
if os.path.exists(file_path):
    with st.spinner("Loading data..."):
        ds = xr.open_dataset(file_path)

        # Assuming the dataset contains temperature or precipitation variables
        variable = st.selectbox("Select Variable:", list(ds.data_vars.keys()))

        data = ds[variable]

        # Plot data
        fig, ax = plt.subplots(figsize=(8, 6))
        data.plot(ax=ax, cmap="gist_stern_r")
        ax.set_title(f"{variable} - {scenario.upper()} {year}")

        st.pyplot(fig)
else:
    st.error("File not found. Please select a different year or scenario.")
