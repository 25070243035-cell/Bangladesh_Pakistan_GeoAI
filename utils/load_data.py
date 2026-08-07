import geopandas as gpd
import streamlit as st


@st.cache_data
def load_geo():

    gdf = gpd.read_file(
        "data/Bangladesh_LISA_CompoundRisk.gpkg"
)
    return gdf


# =====================================================
# NEW — Pakistan loader
# =====================================================

@st.cache_data
def load_geo_pakistan():

    gdf = gpd.read_file(
        "data/Pakistan_Compound_Risk_LISA.gpkg"
    )

    # Rename Pakistan columns so they match the Bangladesh
    # naming convention used by every page module
    # (hazard.py, infrastructure.py, social.py, compound.py,
    # hotspots.py, map_component.py) — this lets us reuse
    # those files as-is for Pakistan too.
    gdf = gdf.rename(
        columns={
            "DISTRICT": "DIST_NAME",
            "SVI": "Social_Vulnerability",
            "IVI": "Infrastructure_Vulnerability",
        }
    )

    return gdf