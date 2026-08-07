import streamlit as st
import plotly.express as px

from components.map_component import show_map


def show_social(gdf):

    st.title("👥 Social Vulnerability")

    st.caption(
        "Bangladesh • 2022 Social Vulnerability Assessment"
    )

    st.write(
        """
Social Vulnerability represents the sensitivity of
communities to disaster impacts.

It considers factors related to population conditions
that influence disaster preparedness, response capacity,
and recovery ability.

Higher values indicate socially vulnerable districts.
"""
    )


    social = gdf[
        gdf["Social_Vulnerability"].notna()
    ].copy()



    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Study Districts",
        len(social)
    )


    c2.metric(
        "Mean Vulnerability",
        round(
            social["Social_Vulnerability"].mean(),
            3
        )
    )


    c3.metric(
        "Maximum Vulnerability",
        round(
            social["Social_Vulnerability"].max(),
            3
        )
    )


    c4.metric(
        "Minimum Vulnerability",
        round(
            social["Social_Vulnerability"].min(),
            3
        )
    )


    st.divider()


    st.subheader(
        "Social Vulnerability Map"
    )


    show_map(
        social,
        "Social_Vulnerability"
    )


    st.divider()


    st.subheader(
        "Top 10 Socially Vulnerable Districts"
    )


    top10 = social[
        [
            "DIST_NAME",
            "Social_Vulnerability"
        ]
    ].sort_values(
        "Social_Vulnerability",
        ascending=False
    ).head(10)



    fig = px.bar(

        top10,

        x="Social_Vulnerability",

        y="DIST_NAME",

        orientation="h",

        color="Social_Vulnerability",

        color_continuous_scale="Purples",

        labels={
            "Social_Vulnerability":
            "Social Vulnerability Score",

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
        "Social Vulnerability Ranking"
    )


    ranking = social[
        [
            "DIST_NAME",
            "Social_Vulnerability"
        ]
    ].copy()


    ranking = ranking.sort_values(
        "Social_Vulnerability",
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
        "Social Vulnerability"
    ]


    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )