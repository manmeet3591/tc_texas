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

        if "tc_mask" in ds.data_vars:
            tc_mask = ds["tc_mask"]

            # Compute the sum of tc_mask for the selected year
            tc_mask_sum = tc_mask.sum().item()

            # Display the sum
            st.metric(label=f"Total tc_mask for {scenario.upper()} {year}", value=tc_mask_sum)

            # Plot tc_mask
            fig, ax = plt.subplots(figsize=(8, 6))
            tc_mask.plot(ax=ax, cmap="gist_stern_r")
            ax.set_title(f"tc_mask - {scenario.upper()} {year}")

            st.pyplot(fig)
        else:
            st.error("Variable 'tc_mask' not found in the dataset.")
else:
    st.error("File not found. Please select a different year or scenario.")
