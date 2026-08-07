'''
import streamlit as st



def show_about():


    st.title(

        "ℹ About the Project"

    )


    st.markdown(

"""
# GeoAI-Based Compound Disaster Intelligence Platform


## Objective

This platform identifies districts exposed to
compound disaster risks by integrating:

- Flood-Heat Hazard

- Infrastructure Vulnerability

- Social Vulnerability



---


## Study Area

**Bangladesh**


The analysis focuses on selected high-risk districts
for disaster vulnerability assessment.



---


## Methodology


### 1. Hazard Assessment

Evaluation of flood and heat hazard exposure.


### 2. Infrastructure Vulnerability

Assessment of vulnerability of critical infrastructure.


### 3. Social Vulnerability

Assessment of community sensitivity and adaptive capacity.


### 4. Compound Risk Index

Integration of:

- 50% Hazard

- 25% Infrastructure Vulnerability

- 25% Social Vulnerability



### 5. Hotspot Identification

Ranking districts based on overall compound risk.



---


## Technologies Used


- Python

- GeoPandas

- Streamlit

- Folium

- Pandas

- GIS



---


## Platform Outputs


The system provides:

✅ Interactive risk maps

✅ District ranking

✅ Vulnerability assessment

✅ Compound risk visualization

✅ Hotspot identification



---


## Purpose

The platform acts as a decision-support tool
for understanding spatial patterns of disaster risk
and supporting preparedness planning.

"""

    )
    '''






import streamlit as st


def show_about():

    st.title("ℹ About This Platform")

    st.markdown("""
### GeoAI Disaster Intelligence Platform

This platform performs district-level assessment of compound flood–heat risk
across Bangladesh using geospatial artificial intelligence techniques.

---

### Study Area

**Country:** Bangladesh

**Reference Year:** **2022**

The platform integrates:

- Natural Hazard Assessment
- Infrastructure Vulnerability
- Social Vulnerability
- Compound Risk Assessment
- Spatial Hotspot Analysis (LISA)
- Decision Support
- Model Validation

---

## Methodology


### 1. Hazard Assessment

Evaluation of flood and heat hazard exposure.


### 2. Infrastructure Vulnerability

Assessment of vulnerability of critical infrastructure.


### 3. Social Vulnerability

Assessment of community sensitivity and adaptive capacity.


### 4. Compound Risk Index

Integration of:

Integration of:

- Equal-weighted average of Hazard, Infrastructure Vulnerability, and Social Vulnerability
- Compound Risk = (Hazard + Infrastructure + Social) / 3



### 5. Hotspot Identification

Ranking districts based on overall compound risk.



---


## Technologies Used


- Python

- GeoPandas

- Streamlit

- Folium

- Pandas

- GIS



---


## Platform Outputs


The system provides:

✅ Interactive risk maps

✅ District ranking

✅ Vulnerability assessment

✅ Compound risk visualization

✅ Hotspot identification



---


## Purpose

The platform acts as a decision-support tool
for understanding spatial patterns of disaster risk
and supporting preparedness planning.

""")