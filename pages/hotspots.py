import streamlit as st
from components.map_component import show_map


def show_hotspots(gdf):
    st.title("🔥 Spatial Hotspot Analysis")

    st.caption(
    "Bangladesh • 2022 Local Moran's I (LISA) Spatial Cluster Analysis"
)
    st.markdown(
        """
This page presents the results of **Local Indicators of Spatial Association (LISA)**,
which identify statistically significant spatial clusters of compound flood risk.

### Cluster Interpretation

- 🔴 **High–High** : High-risk district surrounded by high-risk neighbours (Hotspot)
- 🔵 **Low–Low** : Low-risk district surrounded by low-risk neighbours (Coldspot)
- 🟠 **High–Low** : High-risk spatial outlier
- 🟢 **Low–High** : Low-risk spatial outlier
- ⚪ **Not Significant** : No statistically significant local spatial association

LISA helps distinguish **true spatial hotspots** from districts that merely have
high risk values but are not part of a statistically significant cluster.
"""
    )

    st.divider()

    # -----------------------------
    # Cluster subsets
    # -----------------------------
    high_high = gdf[gdf["Cluster"] == "High-High"].copy()
    low_low = gdf[gdf["Cluster"] == "Low-Low"].copy()
    high_low = gdf[gdf["Cluster"] == "High-Low"].copy()
    low_high = gdf[gdf["Cluster"] == "Low-High"].copy()
    not_sig = gdf[gdf["Cluster"] == "Not Significant"].copy()

    # -----------------------------
    # Summary metrics
    # -----------------------------
    st.subheader("📊 LISA Cluster Summary")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🔴 High-High", len(high_high))
    c2.metric("🔵 Low-Low", len(low_low))
    c3.metric("🟠 High-Low", len(high_low))
    c4.metric("🟢 Low-High", len(low_high))
    c5.metric("⚪ Not Significant", len(not_sig))

    st.divider()

    # -----------------------------
    # Map
    # -----------------------------
    st.subheader("🗺️ LISA Cluster Map")

    st.markdown(
        """
The map below displays the Local Moran's I cluster classification for each district.
Only statistically significant districts are classified as High–High, Low–Low,
High–Low or Low–High. All remaining districts are shown as Not Significant.
"""
    )

    show_map(gdf, "Cluster")

    # -----------------------------
    # Hotspots
    # -----------------------------
    st.divider()
    st.subheader("🔥 Significant Hotspots")

    if high_high.empty:
        st.info("No statistically significant hotspots were identified.")
    else:
        hotspot_table = (
            high_high[
                [
                    "DIST_NAME",
                    "Hazard_Mean",
                    "Infrastructure_Vulnerability",
                    "Social_Vulnerability",
                    "Compound_Risk",
                ]
            ]
            .sort_values("Compound_Risk", ascending=False)
            .rename(
                columns={
                    "DIST_NAME": "District",
                    "Hazard_Mean": "Hazard",
                    "Infrastructure_Vulnerability": "Infrastructure",
                    "Social_Vulnerability": "Social",
                    "Compound_Risk": "Compound Risk",
                }
            )
        )

        st.dataframe(
            hotspot_table,
            use_container_width=True,
            hide_index=True,
        )

    # -----------------------------
    # Coldspots
    # -----------------------------
    st.divider()
    st.subheader("❄️ Significant Coldspots")

    if low_low.empty:
        st.info("No statistically significant coldspots were identified.")
    else:
        coldspot_table = (
            low_low[
                [
                    "DIST_NAME",
                    "Hazard_Mean",
                    "Infrastructure_Vulnerability",
                    "Social_Vulnerability",
                    "Compound_Risk",
                ]
            ]
            .sort_values("Compound_Risk")
            .rename(
                columns={
                    "DIST_NAME": "District",
                    "Hazard_Mean": "Hazard",
                    "Infrastructure_Vulnerability": "Infrastructure",
                    "Social_Vulnerability": "Social",
                    "Compound_Risk": "Compound Risk",
                }
            )
        )

        st.dataframe(
            coldspot_table,
            use_container_width=True,
            hide_index=True,
        )

    # -----------------------------
    # Spatial Outliers
    # -----------------------------
    st.divider()
    st.subheader("🟠🟢 Spatial Outliers")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟠 High–Low")

        if high_low.empty:
            st.info("No High–Low outliers found.")
        else:
            st.dataframe(
                high_low[
                    [
                        "DIST_NAME",
                        "Compound_Risk",
                    ]
                ].rename(
                    columns={
                        "DIST_NAME": "District",
                        "Compound_Risk": "Compound Risk",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with col2:
        st.markdown("### 🟢 Low–High")

        if low_high.empty:
            st.info("No Low–High outliers found.")
        else:
            st.dataframe(
                low_high[
                    [
                        "DIST_NAME",
                        "Compound_Risk",
                    ]
                ].rename(
                    columns={
                        "DIST_NAME": "District",
                        "Compound_Risk": "Compound Risk",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    # -----------------------------
    # Interpretation
    # -----------------------------
    st.divider()

    st.subheader("📖 Interpretation")

    st.info(
        """
**High–High** districts represent statistically significant spatial hotspots where
high compound flood risk is surrounded by neighbouring districts with similarly
high risk. These districts should receive the highest priority for disaster
preparedness, infrastructure investment and climate adaptation planning.

**Low–Low** districts represent statistically significant coldspots with relatively
lower compound risk surrounded by low-risk neighbours.

**High–Low** and **Low–High** clusters indicate spatial outliers where a district
differs substantially from its surrounding districts.

Districts labelled **Not Significant** do not exhibit statistically significant
local spatial clustering at the selected significance level.
"""
    )