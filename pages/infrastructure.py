import streamlit as st
import plotly.express as px

from components.map_component import show_map


def show_infrastructure(gdf):

    st.title("🏗 Infrastructure Vulnerability")

    st.caption(
        "Bangladesh • 2022 Infrastructure Vulnerability Assessment"
    )

    st.write(
        """
Infrastructure Vulnerability represents the sensitivity of
critical infrastructure such as roads, hospitals, schools,
and essential facilities to disaster impacts.

Higher values indicate districts where infrastructure may
experience greater disruption during flood and heat hazards.
"""
    )


    infra = gdf[
        gdf["Infrastructure_Vulnerability"].notna()
    ].copy()


    # KPI Cards

    c1, c2, c3, c4 = st.columns(4)


    c1.metric(
        "Study Districts",
        len(infra)
    )


    c2.metric(
        "Mean Vulnerability",
        round(
            infra["Infrastructure_Vulnerability"].mean(),
            3
        )
    )


    c3.metric(
        "Maximum Vulnerability",
        round(
            infra["Infrastructure_Vulnerability"].max(),
            3
        )
    )


    c4.metric(
        "Minimum Vulnerability",
        round(
            infra["Infrastructure_Vulnerability"].min(),
            3
        )
    )


    st.divider()


    st.subheader(
        "Infrastructure Vulnerability Map"
    )


    show_map(
        infra,
        "Infrastructure_Vulnerability"
    )


    st.divider()


    st.subheader(
        "Top 10 Most Infrastructure Vulnerable Districts"
    )


    top10 = infra[
        [
            "DIST_NAME",
            "Infrastructure_Vulnerability"
        ]
    ].sort_values(
        "Infrastructure_Vulnerability",
        ascending=False
    ).head(10)


    fig = px.bar(
        top10,
        x="Infrastructure_Vulnerability",
        y="DIST_NAME",
        orientation="h",
        color="Infrastructure_Vulnerability",
        color_continuous_scale="Reds",
        labels={
            "Infrastructure_Vulnerability":
            "Infrastructure Vulnerability Score",

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
        "Infrastructure Vulnerability Ranking"
    )


    ranking = infra[
        [
            "DIST_NAME",
            "Infrastructure_Vulnerability"
        ]
    ].copy()


    ranking = ranking.sort_values(
        "Infrastructure_Vulnerability",
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
        "Infrastructure Vulnerability"
    ]


    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True
    )