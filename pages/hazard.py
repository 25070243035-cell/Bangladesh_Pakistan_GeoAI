'''
import streamlit as st
import pandas as pd
import plotly.express as px

from components.map_component import show_map



def show_hazard(gdf):


    st.title(
        "🌧 Natural Hazard Assessment"
    )


    st.write(
        """
This page presents the spatial distribution of
**Flood-Heat Hazard** across Bangladesh districts.
It highlights areas with higher exposure to
natural hazard conditions.
"""
    )


    hazard = gdf[
        gdf["Hazard_Mean"].notna()
    ].copy()



    c1,c2,c3,c4 = st.columns(4)


    c1.metric(
        "Study Districts",
        len(hazard)
    )


    c2.metric(
        "Mean Natural Hazard",
        round(
            hazard["Hazard_Mean"].mean(),
            3
        )
    )


    c3.metric(
        "Maximum Hazard",
        round(
            hazard["Hazard_Mean"].max(),
            3
        )
    )


    c4.metric(
        "Minimum Hazard",
        round(
            hazard["Hazard_Mean"].min(),
            3
        )
    )



    st.divider()



    st.subheader(
        "Flood-Heat Hazard Map"
    )


    show_map(
        hazard,
        "Hazard_Mean"
    )



    st.divider()



    st.subheader(
        "Top 10 Districts by Natural Hazard"
    )


    top10 = hazard[
        [
            "DIST_NAME",
            "Hazard_Mean"
        ]
    ].sort_values(
        "Hazard_Mean",
        ascending=False
    ).head(10)



    fig = px.bar(

        top10,

        x="Hazard_Mean",

        y="DIST_NAME",

        orientation="h",

        color="Hazard_Mean",

        color_continuous_scale="YlOrRd",

        labels={
            "Hazard_Mean":
            "Natural Hazard Score",

            "DIST_NAME":
            "District"
        }

    )


    fig.update_layout(
        height=500,
        yaxis={
            "categoryorder":"total ascending"
        }
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.divider()



    st.subheader(
        "Natural Hazard Ranking"
    )


    ranking = hazard[
        [
            "DIST_NAME",
            "Hazard_Mean"
        ]
    ].copy()



    ranking = ranking.sort_values(
        "Hazard_Mean",
        ascending=False
    )



    ranking.insert(
        0,
        "Rank",
        range(
            1,
            len(ranking)+1
        )
    )



    ranking.columns = [
        "Rank",
        "District",
        "Natural Hazard"
    ]



    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )

'''












import streamlit as st
import pandas as pd
import plotly.express as px

from components.map_component import show_map


def show_hazard(gdf):

    st.title(
        "🌧 Natural Hazard Assessment"
    )

    st.caption(
        "Bangladesh • 2022 Flood–Heat Hazard Assessment"
    )

    st.write(
        """
This page presents the spatial distribution of
**Flood-Heat Hazard** across Bangladesh districts.
It highlights areas with higher exposure to
natural hazard conditions.
"""
    )

    hazard = gdf[
        gdf["Hazard_Mean"].notna()
    ].copy()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Study Districts",
        len(hazard)
    )

    c2.metric(
        "Mean Natural Hazard",
        round(
            hazard["Hazard_Mean"].mean(),
            3
        )
    )

    c3.metric(
        "Maximum Hazard",
        round(
            hazard["Hazard_Mean"].max(),
            3
        )
    )

    c4.metric(
        "Minimum Hazard",
        round(
            hazard["Hazard_Mean"].min(),
            3
        )
    )

    st.divider()

    st.subheader(
        "Flood-Heat Hazard Map"
    )

    show_map(
        hazard,
        "Hazard_Mean"
    )

    st.divider()

    st.subheader(
        "Top 10 Districts by Natural Hazard"
    )

    top10 = hazard[
        [
            "DIST_NAME",
            "Hazard_Mean"
        ]
    ].sort_values(
        "Hazard_Mean",
        ascending=False
    ).head(10)

    fig = px.bar(

        top10,

        x="Hazard_Mean",

        y="DIST_NAME",

        orientation="h",

        color="Hazard_Mean",

        color_continuous_scale="YlOrRd",

        labels={
            "Hazard_Mean":
            "Natural Hazard Score",

            "DIST_NAME":
            "District"
        }

    )

    fig.update_layout(
        height=500,
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader(
        "Natural Hazard Ranking"
    )

    ranking = hazard[
        [
            "DIST_NAME",
            "Hazard_Mean"
        ]
    ].copy()

    ranking = ranking.sort_values(
        "Hazard_Mean",
        ascending=False
    )

    ranking.insert(
        0,
        "Rank",
        range(
            1,
            len(ranking) + 1
        )
    )

    ranking.columns = [
        "Rank",
        "District",
        "Natural Hazard"
    ]

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )