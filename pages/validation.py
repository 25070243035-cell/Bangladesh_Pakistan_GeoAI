import streamlit as st
import pandas as pd

# --------------------------------------------------------
# DATA PATHS (per country, per hazard)
# --------------------------------------------------------

DATA_PATHS = {
    "Bangladesh": {
        "Flood": "data/Flood_Threshold_Area_Comparison.csv",
        "Heat": "data/Heat_Threshold_Area_Comparison.csv",
        "Compound": "data/Compound_Threshold_Area_Comparison.csv",
    },
    "Pakistan": {
        "Flood": "data/Pakistan_Flood_Threshold_Area_Comparison.csv",
        "Heat": "data/Pakistan_Heat_Threshold_Area_Comparison.csv",
        "Compound": "data/Pakistan_Compound_Threshold_Area_Comparison.csv",
    },
}


# --------------------------------------------------------
# LOAD DATA
# --------------------------------------------------------

@st.cache_data
def load_threshold_table(country, hazard):
    path = DATA_PATHS[country][hazard]
    return pd.read_csv(path)


# --------------------------------------------------------
# INTERPRETATION
# --------------------------------------------------------

def threshold_message(country, hazard, row):

    threshold = row["Threshold"]

    if country == "Bangladesh":

        if hazard == "Flood":

            if threshold == 0.86:
                st.success("""
### ✅ Recommended Bangladesh Threshold

This threshold provides the closest match between the predicted and observed
flood extent in Bangladesh.

• Actual Flood Area : **7541 km²**

• Predicted Flood Area : **7571 km²**

• Difference : **30 km²**

Although the F1-score is slightly lower than some other thresholds,
the spatial agreement with the observed flood extent is the best,
making it the recommended operational threshold for Bangladesh.
""")

            elif threshold == 0.55:
                st.warning("""
### ⚠ Pakistan Threshold

Threshold **0.55** was selected during the Pakistan model development.

When applied directly to Bangladesh, it predicts substantially larger
flood extent than actually observed.

Therefore, this threshold is **not ideal for Bangladesh** despite
having a relatively good F1-score.
""")

            else:
                st.info("""
This threshold is presented for sensitivity analysis.

Different thresholds produce different flood extents and model
performance. Threshold selection depends on the intended application.
""")

        elif hazard == "Heat":

            if threshold == 0.06:
                st.success("""
### ✅ Recommended Bangladesh Threshold

This threshold provides the closest match between predicted and observed
heat extent in Bangladesh.

It was therefore selected for the final Bangladesh heat analysis.
""")

            elif threshold == 0.55:
                st.warning("""
### ⚠ Pakistan Threshold

The original Pakistan threshold performs poorly over Bangladesh and
significantly underestimates heat extent.
""")

            else:
                st.info("""
Shown for threshold sensitivity comparison.
""")

        elif hazard == "Compound":

            if threshold == 0.13:
                st.success("""
### ✅ Recommended Bangladesh Threshold

This threshold best reproduces the observed compound hazard extent.

It provides the smallest spatial difference and was therefore selected
for the final compound hazard mapping.
""")

            elif threshold == 0.55:
                st.warning("""
### ⚠ Pakistan Threshold

The Pakistan threshold greatly underestimates compound hazard over
Bangladesh and is not recommended.
""")

            else:
                st.info("""
Shown for sensitivity analysis.
""")

    elif country == "Pakistan":

        reason = row.get("Threshold_Reason", "")

        detail = f"""
• Precision : **{row['Precision']:.3f}**

• Recall : **{row['Recall']:.3f}**

• F1-score : **{row['F1_score']:.4f}**

• Over/Under-prediction : **{row['Over_Under_prediction_%']:.1f}%**
"""

        if reason == "Project-selected threshold":
            st.success(f"""
### ✅ Project-Selected Threshold

Threshold **{threshold}** was selected via nested spatial cross-validation
as the operating threshold for the {hazard} hazard on the Pakistan training
domain (Section 4.7). This is the threshold exported for external
validation on Bangladesh.
{detail}
""")

        elif reason == "Best F1-score threshold":
            st.info(f"""
### 📈 Best F1-Score Threshold

Threshold **{threshold}** maximises the F1-score for {hazard} on the
Pakistan training domain, but was not the threshold ultimately selected
for operational use (see the Project-Selected Threshold above).
{detail}
""")

        elif reason == "Best area-matched threshold":
            st.info(f"""
### 📐 Best Area-Matched Threshold

Threshold **{threshold}** most closely reproduces the observed
{hazard.lower()} extent by area for the Pakistan training domain.
{detail}
""")

        elif reason == "Standard threshold":
            st.info(f"""
### ⚖ Standard Threshold

Threshold **{threshold}** (the conventional 0.5 default) is shown for
comparison against the project-selected operating threshold.
{detail}
""")

        elif reason == "Sensitivity threshold":
            st.info(f"""
### 🔍 Sensitivity Threshold

Threshold **{threshold}** is shown for sensitivity analysis on the
Pakistan training domain.
{detail}
""")

        else:
            st.info(f"""
### {reason or 'Sensitivity Analysis'}

Threshold **{threshold}** is shown for sensitivity comparison across the
Pakistan training domain.
{detail}
""")


# --------------------------------------------------------
# MAIN PAGE
# --------------------------------------------------------

def show_validation(country="Bangladesh"):

    st.title("📊 Model Validation & Threshold Analysis")

    st.caption(
        f"{country} • {'External Validation' if country == 'Bangladesh' else 'Training Domain'} • 2022"
    )

    st.write(
        """
The CatBoost model produces probabilities rather than direct hazard labels.

A decision threshold converts these probabilities into hazard classes.

Different thresholds produce different hazard extents, therefore selecting an
appropriate threshold is essential for accurate mapping.
"""
    )

    hazard = st.radio(
        "Select Hazard",
        ["Flood", "Heat", "Compound"],
        horizontal=True,
        key=f"{country}_hazard_radio"
    )

    table = load_threshold_table(country, hazard)

    st.divider()

    st.subheader("Threshold Comparison")

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    thresholds = sorted(table["Threshold"].unique())

    selected = st.selectbox(
        "Select Threshold",
        thresholds,
        key=f"{country}_threshold_select"
    )

    row = table[table["Threshold"] == selected].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Actual Area",
        f"{row['Actual_km2']:,} km²"
    )

    c2.metric(
        "Predicted Area",
        f"{row['Predicted_km2']:,} km²"
    )

    c3.metric(
        "Difference",
        f"{abs(row['Difference_pixels']):,}"
    )

    c4.metric(
        "F1 Score",
        f"{row['F1_score']:.3f}"
    )

    threshold_message(country, hazard, row)

    st.divider()

    st.info(
        """
### Why do different thresholds produce different results?

Machine learning models predict probabilities between **0 and 1**.

A threshold determines the probability above which a pixel is classified
as hazardous.

- Lower thresholds classify more pixels as hazardous and generally increase Recall.
- Higher thresholds classify fewer pixels as hazardous and generally reduce False Positives.
- Therefore, different thresholds produce different mapped hazard extents and performance metrics.

For this project, thresholds were selected based on **their ability to reproduce the observed hazard extent**, rather than simply maximizing the F1-score.
"""
    )