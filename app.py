import streamlit as st
from streamlit_option_menu import option_menu

from utils.load_data import load_geo, load_geo_pakistan

from pages.hazard import show_hazard
from pages.infrastructure import show_infrastructure
from pages.social import show_social
from pages.compound import show_compound
from pages.hotspots import show_hotspots
from pages.about import show_about
from pages.validation import show_validation

from components.home_map import show_home_map


st.set_page_config(
    page_title="Bangladesh GeoAI Platform",
    page_icon="🌏",
    layout="wide"
)


# -------------------------------
# Risk Category (shared helper)
# -------------------------------

def risk_category(x):

    if x >= 0.40:
        return "Very High"

    elif x >= 0.30:
        return "High"

    elif x >= 0.20:
        return "Moderate"

    else:
        return "Low"


# =====================================================
# NEW — COUNTRY SELECTOR (top-level tab, above everything)
# =====================================================

country = option_menu(
    None,
    ["Bangladesh", "Pakistan"],
    icons=["flag", "flag"],
    orientation="horizontal",
    key="country_menu",
    styles={
        "container": {
            "padding": "4px",
            "background-color": "#f5f5f5",
            "border-radius": "8px",
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "2px",
            "background-color": "#E9ECEF",   # Light gray
            "color": "black",
            "border": "1px solid #BDBDBD",
            "border-radius": "6px",
            "--hover-color": "#D6D6D6",
        },
        "nav-link-selected": {
            "background-color": "#FFD700",   # Yellow
            "color": "black",
            "font-weight": "bold",
            "border": "1px solid #D4AC0D",
        },
    },
)


# =====================================================================
# ============================ BANGLADESH ============================
# =====================================================================
# Everything in this block is your ORIGINAL app.py logic, unchanged,
# just indented under "if country == 'Bangladesh':"
# =====================================================================

if country == "Bangladesh":

    # -------------------------------
    # Navigation
    # -------------------------------

    selected = option_menu(
        None,
        [
            "Home",
            "Flood-Heat Hazard",
            "Infrastructure",
            "Social",
            "Compound Risk",
            "Hotspots",
            "Model Validation",
            "About"
        ],
        icons=[
            "house",
            "cloud-rain",
            "building",
            "people",
            "exclamation-triangle",
            "geo-alt",
            "clipboard-data",
            "info-circle"
        ],
        orientation="horizontal",
        key="bd_menu"
    )

    # -------------------------------
    # Load Data
    # -------------------------------

    gdf = load_geo()

    compound = gdf[
        gdf["Compound_Risk"].notna()
    ].copy()

    compound["Risk_Category"] = compound[
        "Compound_Risk"
    ].apply(risk_category)

    # -------------------------------
    # Sidebar
    # -------------------------------

    st.sidebar.title("🌏 GeoAI Disaster Platform")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Study Information")
    st.sidebar.info("""
**Country:** Bangladesh

**Reference Year:** **2022**

**Study:** Compound Flood–Heat Risk Assessment
""")

    st.sidebar.markdown(
"""
### Bangladesh

Compound Disaster Risk Assessment

Explore:

🌧 Flood-Heat Hazard

🏥 Infrastructure Vulnerability

👥 Social Vulnerability

⚠ Compound Risk

🔥 Hotspots
"""
    )

    st.sidebar.divider()

    district_search = st.sidebar.text_input(
        "🔎 Search District",
        key="bd_search"
    )

    if district_search:

        result = gdf[
            gdf["DIST_NAME"]
            .str.contains(
                district_search,
                case=False,
                na=False
            )
        ]

        if len(result) > 0:

            st.sidebar.success(
                f"{len(result)} district found"
            )

        else:

            st.sidebar.warning(
                "No district found"
            )

    # -------------------------------
    # Risk Badge
    # -------------------------------

    def risk_badge(value):

        if value >= 0.40:
            return "🔴 Very High Risk"

        elif value >= 0.30:
            return "🟠 High Risk"

        elif value >= 0.20:
            return "🟡 Moderate Risk"

        else:
            return "🟢 Low Risk"

    # ===============================
    # HOME
    # ===============================

    if selected == "Home":

        st.title("🌏 GeoAI Disaster Intelligence Platform")

        st.caption(
            "Bangladesh Compound Flood–Heat Hazard, Vulnerability and Spatial Risk Assessment • **Reference Year: 2022**"
        )

        st.info(
            """
📅 **Reference Year:** 2022

This platform analyses Bangladesh districts using geospatial indicators representing the 2022 monsoon flood and heat conditions.
"""
        )

        st.markdown(
"""
## Bangladesh Disaster Risk Assessment

This platform integrates geospatial analysis to evaluate
compound disaster risk across Bangladesh districts.

The assessment combines:

- 🌧 Flood-Heat Hazard

- 🏥 Infrastructure Vulnerability

- 👥 Social Vulnerability

to identify districts requiring improved disaster
preparedness and mitigation planning.
"""
        )

        st.divider()

        st.subheader(
            "🗺 Study Area: Bangladesh"
        )

        show_home_map(gdf)

        st.divider()

        st.subheader(
            "🔬 Assessment Framework"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.info(
"""
### 🌧 Flood-Heat Hazard

Measures exposure to natural hazards,
including flood and heat-related impacts.
"""
            )

            st.warning(
"""
### 🏥 Infrastructure Vulnerability

Evaluates sensitivity of critical
infrastructure systems.
"""
            )

        with c2:

            st.success(
"""
### 👥 Social Vulnerability

Represents community sensitivity and
capacity to cope with disasters.
"""
            )

            st.error(
"""
### ⚠ Compound Risk

Integrated index:

50% Hazard

25% Infrastructure

25% Social Vulnerability
"""
            )

        st.divider()

        st.subheader(
            "🔥 Hotspot Analysis"
        )

        st.write(
"""
High-risk districts are identified using
compound risk ranking.

These locations can support:

- Disaster planning
- Resource allocation
- Risk reduction strategies
"""
        )

    # ===============================
    # OTHER PAGES
    # ===============================

    elif selected == "Flood-Heat Hazard":

        show_hazard(gdf)

    elif selected == "Infrastructure":

        show_infrastructure(gdf)

    elif selected == "Social":

        show_social(gdf)

    elif selected == "Compound Risk":

        show_compound(gdf)

    elif selected == "Hotspots":

        show_hotspots(gdf)

    elif selected == "Model Validation":
        show_validation()

    elif selected == "About":

        show_about()


# =====================================================================
# ============================= PAKISTAN =============================
# =====================================================================
# NEW — mirrors the Bangladesh block above, reusing the SAME page
# modules (hazard.py, infrastructure.py, social.py, compound.py,
# hotspots.py) since load_geo_pakistan() renames columns to match.
#
# "Model Validation" is skipped for Pakistan since there is no
# equivalent Flood/Heat/Compound threshold comparison CSV for it yet.
# Add it back the same way as Bangladesh once that data exists.
# =====================================================================

elif country == "Pakistan":

    # -------------------------------
    # Navigation
    # -------------------------------

    selected_pk = option_menu(
        None,
        [
            "Home",
            "Flood-Heat Hazard",
            "Infrastructure",
            "Social",
            "Compound Risk",
            "Hotspots",
            "Model Validation",
            "About"
        ],
        icons=[
            "house",
            "cloud-rain",
            "building",
            "people",
            "exclamation-triangle",
            "geo-alt",
            "clipboard-data",
            "info-circle"
        ],
        orientation="horizontal",
        key="pk_menu"
    )

    # -------------------------------
    # Load Data
    # -------------------------------

    pk_gdf = load_geo_pakistan()

    pk_compound = pk_gdf[
        pk_gdf["Compound_Risk"].notna()
    ].copy()

    pk_compound["Risk_Category"] = pk_compound[
        "Compound_Risk"
    ].apply(risk_category)

    # -------------------------------
    # Sidebar
    # -------------------------------

    st.sidebar.title("🌏 GeoAI Disaster Platform")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Study Information")
    st.sidebar.info("""
**Country:** Pakistan

**Study:** Compound Flood–Heat Risk Assessment
""")

    st.sidebar.markdown(
"""
### Pakistan

Compound Disaster Risk Assessment

Explore:

🌧 Flood-Heat Hazard

🏥 Infrastructure Vulnerability

👥 Social Vulnerability

⚠ Compound Risk

🔥 Hotspots
"""
    )

    st.sidebar.divider()

    district_search_pk = st.sidebar.text_input(
        "🔎 Search District",
        key="pk_search"
    )

    if district_search_pk:

        result_pk = pk_gdf[
            pk_gdf["DIST_NAME"]
            .str.contains(
                district_search_pk,
                case=False,
                na=False
            )
        ]

        if len(result_pk) > 0:

            st.sidebar.success(
                f"{len(result_pk)} district found"
            )

        else:

            st.sidebar.warning(
                "No district found"
            )

    # ===============================
    # HOME
    # ===============================

    if selected_pk == "Home":

        st.title("🌏 GeoAI Disaster Intelligence Platform")

        st.caption(
            "Pakistan Compound Flood–Heat Hazard, Vulnerability and Spatial Risk Assessment"
        )

        st.markdown(
"""
## Pakistan Disaster Risk Assessment

This platform integrates geospatial analysis to evaluate
compound disaster risk across Pakistan districts.

The assessment combines:

- 🌧 Flood-Heat Hazard

- 🏥 Infrastructure Vulnerability

- 👥 Social Vulnerability

to identify districts requiring improved disaster
preparedness and mitigation planning.
"""
        )

        st.divider()

        st.subheader(
            "🗺 Study Area: Pakistan"
        )

        show_home_map(pk_gdf)

        st.divider()

        st.subheader(
            "🔬 Assessment Framework"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.info(
"""
### 🌧 Flood-Heat Hazard

Measures exposure to natural hazards,
including flood and heat-related impacts.
"""
            )

            st.warning(
"""
### 🏥 Infrastructure Vulnerability

Evaluates sensitivity of critical
infrastructure systems.
"""
            )

        with c2:

            st.success(
"""
### 👥 Social Vulnerability

Represents community sensitivity and
capacity to cope with disasters.
"""
            )

            st.error(
"""
### ⚠ Compound Risk

Integrated index:

Combines normalized Hazard, SVI and IVI
"""
            )

        st.divider()

        st.subheader(
            "🔥 Hotspot Analysis"
        )

        st.write(
"""
High-risk districts are identified using
compound risk ranking.

These locations can support:

- Disaster planning
- Resource allocation
- Risk reduction strategies
"""
        )

    # ===============================
    # OTHER PAGES (reusing Bangladesh page modules)
    # ===============================

    elif selected_pk == "Flood-Heat Hazard":

        show_hazard(pk_gdf)

    elif selected_pk == "Infrastructure":

        show_infrastructure(pk_gdf)

    elif selected_pk == "Social":

        show_social(pk_gdf)

    elif selected_pk == "Compound Risk":

        show_compound(pk_gdf)

    elif selected_pk == "Hotspots":

        show_hotspots(pk_gdf)

    elif selected_pk == "Model Validation":

        show_validation("Pakistan")

    elif selected_pk == "About":

        st.title("ℹ About This Platform")

        st.markdown("""
### GeoAI Disaster Intelligence Platform

This platform performs district-level assessment of compound flood–heat risk
across Pakistan using geospatial artificial intelligence techniques.

---

### Study Area

**Country:** Pakistan

The platform integrates:

- Natural Hazard Assessment
- Infrastructure Vulnerability (IVI)
- Social Vulnerability (SVI)
- Compound Risk Assessment
- Spatial Hotspot Analysis (LISA)
- Decision Support

---

## Methodology

### 1. Hazard Assessment

Evaluation of flood and heat hazard exposure using a compound
hazard probability raster.

### 2. Infrastructure Vulnerability (IVI)

Combines road density, health facility density, school density,
electricity and water access indicators.

### 3. Social Vulnerability (SVI)

Combines population density, dependency ratio, literacy,
sanitation and food security indicators.

### 4. Compound Risk Index

Average of normalized Hazard, IVI and SVI.

### 5. Hotspot Identification (LISA)

Local Moran's I clustering of district-level compound risk.
""")


# -------------------------------
# Footer
# -------------------------------

st.divider()

st.caption(
"""
GeoAI-Based Compound Disaster Intelligence Platform |
Python | GeoPandas | Folium | Streamlit
"""
)