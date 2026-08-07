import folium
import streamlit as st
from streamlit_folium import st_folium

# ---------------------------------------------------
# LISA Cluster Colours
# ---------------------------------------------------

LISA_COLORS = {
    "High-High": "#d73027",        # Red
    "Low-Low": "#4575b4",          # Blue
    "High-Low": "#fdae61",         # Orange
    "Low-High": "#66bd63",         # Green
    "Not Significant": "#d9d9d9"  # Grey
}


def show_map(gdf, column):
    # Create map
    m = folium.Map(
        location=[24.2, 90.2],
        zoom_start=7,
        tiles="CartoDB positron"
    )

    # Fit map to data
    bounds = [
        [gdf.total_bounds[1], gdf.total_bounds[0]],
        [gdf.total_bounds[3], gdf.total_bounds[2]]
    ]
    m.fit_bounds(bounds)

    # ------------------------------------------
    # Style Function
    # ------------------------------------------
    def style_function(feature):
        value = feature["properties"][column]

        # LISA Cluster Colours
        if column == "Cluster":
            color = LISA_COLORS.get(value, "#d9d9d9")
            return {
                "fillColor": color,
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.8,
            }

        # Continuous colour ramp
        min_val = gdf[column].min()
        max_val = gdf[column].max()

        ratio = (value - min_val) / (max_val - min_val + 1e-9)

        if ratio >= 0.75:
            color = "#800026"
        elif ratio >= 0.50:
            color = "#FC4E2A"
        elif ratio >= 0.25:
            color = "#FD8D3C"
        else:
            color = "#FED976"

        return {
            "fillColor": color,
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.8,
        }

    # ------------------------------------------
    # GeoJSON Layer
    # ------------------------------------------
    folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=lambda x: {
            "weight": 3,
            "color": "black",
            "fillOpacity": 1,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=[
                "DIST_NAME",
                "Cluster",
                "Compound_Risk",
            ],
            aliases=[
                "District",
                "LISA Cluster",
                "Compound Risk",
            ],
            localize=True,
            sticky=False,
        ),
    ).add_to(m)

    # ------------------------------------------
    # District Labels
    # ------------------------------------------
    for _, row in gdf.iterrows():
        point = row.geometry.representative_point()

        folium.Marker(
            location=[point.y, point.x],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size:10px;
                    font-weight:bold;
                    color:black;
                    text-align:center;
                    white-space:nowrap;
                    text-shadow:
                        1px 1px white,
                        -1px -1px white,
                        1px -1px white,
                        -1px 1px white;
                ">
                {row['DIST_NAME']}
                </div>
                """
            ),
        ).add_to(m)

    # ------------------------------------------
    # Legend
    # ------------------------------------------
    if column == "Cluster":

        legend = """
        <div style="
        position:fixed;
        bottom:30px;
        left:30px;
        background:white;
        padding:15px;
        border-radius:8px;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        width:240px;
        ">

        <b>LISA Cluster Map</b>
        <hr>

        <span style="background:#d73027;width:18px;height:18px;display:inline-block;"></span>
        High-High (Hotspot)

        <br><br>

        <span style="background:#4575b4;width:18px;height:18px;display:inline-block;"></span>
        Low-Low (Coldspot)

        <br><br>

        <span style="background:#fdae61;width:18px;height:18px;display:inline-block;"></span>
        High-Low

        <br><br>

        <span style="background:#66bd63;width:18px;height:18px;display:inline-block;"></span>
        Low-High

        <br><br>

        <span style="background:#d9d9d9;width:18px;height:18px;display:inline-block;"></span>
        Not Significant

        </div>
        """

    else:

        legend = f"""
        <div style="
        position:fixed;
        bottom:30px;
        left:30px;
        background:white;
        padding:15px;
        border-radius:8px;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        width:220px;
        ">

        <b>{column.replace('_', ' ')}</b>
        <hr>

        <span style="background:#FED976;width:18px;height:18px;display:inline-block;"></span>
        Low

        <br><br>

        <span style="background:#FD8D3C;width:18px;height:18px;display:inline-block;"></span>
        Moderate

        <br><br>

        <span style="background:#FC4E2A;width:18px;height:18px;display:inline-block;"></span>
        High

        <br><br>

        <span style="background:#800026;width:18px;height:18px;display:inline-block;"></span>
        Very High

        </div>
        """

    # Add legend
    m.get_root().html.add_child(folium.Element(legend))

    # ------------------------------------------
    # Download HTML
    # ------------------------------------------
    html = m.get_root().render()

    st.download_button(
        label="📥 Download Map (HTML)",
        data=html,
        file_name=f"{column}_map.html",
        mime="text/html",
    )

    # ------------------------------------------
    # Display Map
    # ------------------------------------------
    st_folium(
        m,
        width=1200,
        height=650,
    )