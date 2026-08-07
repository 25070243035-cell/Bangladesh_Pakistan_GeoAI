import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.map_component import show_map
from utils.advisory import generate_advisory, get_priority


def show_compound(gdf):

    st.title(
        "⚠ Compound Risk Assessment"
    )

    st.caption(
        "Bangladesh • 2022 Compound Flood–Heat Risk Assessment"
    )

    st.write(
        """
Compound Disaster Risk represents the combined impact
of natural hazards, infrastructure vulnerability,
and social vulnerability.

The index integrates:

- 🌧 Natural Hazard Exposure
- 🏥 Infrastructure Vulnerability
- 👥 Social Vulnerability

Higher values indicate districts requiring greater
priority for disaster preparedness and mitigation.
"""
    )

    compound = gdf[
        gdf["Compound_Risk"].notna()
    ].copy()


    # ==========================================================
    # KPI CARDS
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Study Districts",
        len(compound)
    )

    c2.metric(
        "Mean Compound Risk",
        round(
            compound["Compound_Risk"].mean(),
            3
        )
    )

    c3.metric(
        "Maximum Risk",
        round(
            compound["Compound_Risk"].max(),
            3
        )
    )

    c4.metric(
        "Minimum Risk",
        round(
            compound["Compound_Risk"].min(),
            3
        )
    )


    st.divider()


    # ==========================================================
    # RISK CATEGORY
    # ==========================================================

    def risk_category(x):

        if x >= 0.40:
            return "Very High"

        elif x >= 0.30:
            return "High"

        elif x >= 0.20:
            return "Moderate"

        else:
            return "Low"


    compound["Risk_Category"] = compound[
        "Compound_Risk"
    ].apply(
        risk_category
    )


    category_count = (
        compound["Risk_Category"]
        .value_counts()
        .reset_index()
    )


    category_count.columns = [
        "Risk Category",
        "District Count"
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "Risk Category Distribution"
        )


        fig = px.pie(

            category_count,

            names="Risk Category",

            values="District Count",

            color="Risk Category",

            color_discrete_map={

                "Very High": "#800026",

                "High": "#FC4E2A",

                "Moderate": "#FD8D3C",

                "Low": "#FED976"

            }

        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        st.subheader(
            "Risk Composition"
        )


        st.info(
            """
Compound Risk Formula:

Equal-weighted average of:

🌧 Natural Hazard
🏥 Infrastructure Vulnerability
👥 Social Vulnerability

Compound Risk = (Hazard + Infrastructure + Social) / 3
"""
        )


    st.divider()


    # ==========================================================
    # MAP
    # ==========================================================

    st.subheader(
        "Compound Risk Map"
    )


    show_map(

        compound,

        "Compound_Risk"

    )


    st.divider()


        # ==========================================================
    # DISTRICT RANKING
    # ==========================================================

    st.subheader(
        "District Risk Ranking"
    )


    ranking = compound[

        [

            "DIST_NAME",

            "Hazard_Mean",

            "Infrastructure_Vulnerability",

            "Social_Vulnerability",

            "Compound_Risk",

            "Risk_Category"

        ]

    ].copy()


    ranking = ranking.sort_values(

        "Compound_Risk",

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

        "Natural Hazard",

        "Infrastructure",

        "Social",

        "Compound Risk",

        "Risk Category"

    ]


    highest = ranking.iloc[0]

    lowest = ranking.iloc[-1]


    col1, col2 = st.columns(2)


    with col1:

        st.success(

            f"""
Highest Risk District

**{highest['District']}**

Compound Risk:

**{highest['Compound Risk']:.3f}**
"""

        )


    with col2:

        st.info(

            f"""
Lowest Risk District

**{lowest['District']}**

Compound Risk:

**{lowest['Compound Risk']:.3f}**
"""

        )


    st.dataframe(

        ranking,

        use_container_width=True,

        hide_index=True

    )


    st.divider()


    # ==========================================================
    # DECISION SUPPORT SYSTEM
    # ==========================================================

    st.header(
        "🧭 Decision Support System"
    )


    st.markdown(
        """
Select a district to receive decision-support recommendations based on its
Natural Hazard, Infrastructure Vulnerability, Social Vulnerability and
overall Compound Risk.

The recommendations assist disaster managers in prioritizing preparedness
and mitigation strategies.
"""
    )


    district = st.selectbox(

        "Select District",

        ranking["District"].tolist()

    )


    row = compound[

        compound["DIST_NAME"] == district

    ].iloc[0]


    priority, icon = get_priority(

        row["Compound_Risk"]

    )


    st.divider()


    left, right = st.columns(
        [1, 1]
    )


    # ==========================================================
    # LEFT PANEL
    # ==========================================================

    with left:


        st.subheader(
            "📈 Risk Summary"
        )


        c1, c2 = st.columns(2)


        c1.metric(

            "Compound Risk",

            f"{row['Compound_Risk']:.3f}"

        )


        c2.metric(

            "Priority",

            priority

        )


        # ======================================================
        # NEW RISK DRIVER CONTRIBUTION CHART
        # ======================================================

        st.subheader(
            "📊 Risk Driver Contribution"
        )


        driver_df = pd.DataFrame({

            "Component": [

                "Natural Hazard",

                "Infrastructure",

                "Social"

            ],

            "Score": [

                row["Hazard_Mean"],

                row["Infrastructure_Vulnerability"],

                row["Social_Vulnerability"]

            ]

        })


        fig = px.bar(

            driver_df,

            x="Score",

            y="Component",

            orientation="h",

            text="Score",

            color="Score",

            color_continuous_scale="YlOrRd"

        )


        fig.update_layout(

            height=320,

            coloraxis_showscale=False,

            xaxis_title="Contribution Score",

            yaxis_title=""

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )


        st.subheader(
            "Risk Drivers"
        )


        st.write(
            "🌧 Natural Hazard"
        )


        st.progress(

            float(row["Hazard_Mean"])

        )


        st.caption(

            f"{row['Hazard_Mean']:.3f}"

        )


        st.write(
            "🏗 Infrastructure Vulnerability"
        )


        st.progress(

            float(row["Infrastructure_Vulnerability"])

        )


        st.caption(

            f"{row['Infrastructure_Vulnerability']:.3f}"

        )


        st.write(
            "👥 Social Vulnerability"
        )


        st.progress(

            float(row["Social_Vulnerability"])

        )


        st.caption(

            f"{row['Social_Vulnerability']:.3f}"

        )


    # ==========================================================
    # RIGHT PANEL
    # ==========================================================

    with right:


        if priority == "Critical":


            st.error(

                f"""
# 🔴 CRITICAL

Immediate intervention recommended.

District:

**{district}**
"""

            )


        elif priority == "High":


            st.warning(

                f"""
# 🟠 HIGH

Preparedness measures should be strengthened.

District:

**{district}**
"""

            )


        elif priority == "Moderate":


            st.info(

                f"""
# 🟡 MODERATE

Continuous monitoring recommended.

District:

**{district}**
"""

            )


        else:


            st.success(

                f"""
# 🟢 LOW

Routine monitoring is sufficient.

District:

**{district}**
"""

            )


    st.divider()


        # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    st.subheader(
        "📋 Recommended Actions"
    )


    recommendations = generate_advisory(

        row["Hazard_Mean"],

        row["Infrastructure_Vulnerability"],

        row["Social_Vulnerability"],

        row["Compound_Risk"]

    )


    for rec in recommendations:


        with st.expander(

            f"{rec['icon']} {rec['title']}",

            expanded=True

        ):

            st.write(
                rec["text"]
            )


    st.divider()


    # ==========================================================
    # NEW ACTION TIMELINE
    # ==========================================================

    st.subheader(
        "🗓 Suggested Action Timeline"
    )


    timeline = pd.DataFrame({

        "Time Frame":[

            "Immediate (0–7 Days)",

            "Short Term (1–6 Months)",

            "Long Term (>6 Months)"

        ],

        "Recommended Action":[

            "Preparedness, Early Warning, Emergency Planning",

            "Infrastructure Upgrades, Capacity Building",

            "Policy Planning, Climate Adaptation"

        ]

    })


    st.table(
        timeline
    )


    st.divider()


    # ==========================================================
    # SCORE INTERPRETATION
    # ==========================================================

    st.subheader(
        "📖 Interpretation"
    )


    if row["Compound_Risk"] >= 0.40:


        st.error(

            """
This district exhibits a **very high compound disaster risk**.

Disaster management agencies should prioritize preparedness,
resource allocation, and mitigation planning.
"""

        )


    elif row["Compound_Risk"] >= 0.30:


        st.warning(

            """
This district has a **high compound risk**.

Preventive planning and continuous monitoring are recommended.
"""

        )


    elif row["Compound_Risk"] >= 0.20:


        st.info(

            """
This district has a **moderate compound risk**.

Routine preparedness and periodic monitoring should continue.
"""

        )


    else:


        st.success(

            """
This district currently shows a relatively **low compound risk**.

Standard monitoring procedures are sufficient.
"""

        )


    st.divider()


    # ==========================================================
    # NEW DISTRICT SUMMARY CARD
    # ==========================================================

    st.subheader(
        "📌 District Summary"
    )


    st.info(

        f"""
**District:** {district}


**Compound Risk:** {row['Compound_Risk']:.3f}


**Natural Hazard:** {row['Hazard_Mean']:.3f}


**Infrastructure Vulnerability:** {row['Infrastructure_Vulnerability']:.3f}


**Social Vulnerability:** {row['Social_Vulnerability']:.3f}


**Priority Level:** {priority}
"""

    )


    st.divider()


    # ==========================================================
    # DOWNLOAD RESULTS
    # ==========================================================

    csv = ranking.to_csv(

        index=False

    )


    st.download_button(

        label="📥 Download Compound Risk Results",

        data=csv,

        file_name="compound_risk_2022.csv",

        mime="text/csv"

    )