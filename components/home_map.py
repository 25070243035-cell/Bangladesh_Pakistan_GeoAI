import folium
from streamlit_folium import st_folium


def show_home_map(gdf):

    m = folium.Map(
        location=[24.2, 90.2],
        tiles="CartoDB positron"
    )


    bounds = [
        [gdf.total_bounds[1], gdf.total_bounds[0]],
        [gdf.total_bounds[3], gdf.total_bounds[2]]
    ]


    m.fit_bounds(bounds)



    folium.GeoJson(

        gdf,

        style_function=lambda feature: {

            "fillColor": "#4CAF50",

            "color": "black",

            "weight": 1,

            "fillOpacity": 0.35

        },

        tooltip=folium.GeoJsonTooltip(

            fields=[
                "DIST_NAME"
            ],

            aliases=[
                "District"
            ],

            sticky=False

        ),

        name="Bangladesh Districts"

    ).add_to(m)



    st_folium(

        m,

        width=1100,

        height=550

    )