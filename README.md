# IRDash – Interactive Dashboard for kdr Mutation Frequencies in *Aedes albopictus* (Italy, 2023–2025)

This repository contains the source code for **IRDash**, an interactive web dashboard designed to visualize the spatial and temporal patterns of two key knockdown resistance (kdr) mutations—**V1016G** and **F1534C**—in *Aedes albopictus* populations across Italy.  
The dashboard supports national-scale analyses of pyrethroid resistance and is aligned with FAIR data principles.

**Live dashboard:** http://dspmi.irdash.med.uniroma1.it/

---

## Background

The dataset behind this dashboard was produced by the **Mosquito Insecticide Resistance Italian Network (MosqIRIT)** within the national INF-ACT project (RN2).  
It includes:

- Genotyping data for **3,503 specimens**
- Sampled in **104 out of 107 Italian provinces**
- Collected between **2023 and 2025**
- Frequencies for the **V1016G** and **F1534C** mutations
- Metadata on sampling location, administrative levels, developmental stage, and collection method
- Province-level aggregated mutation frequencies
- Geographic, eco-climatic, and demographic contextual data

These data support public health surveillance, mosquito control programs, and ecological modeling.

---

## Dashboard Features

The dashboard was built with **Dash (v3.0.4)** and **Plotly (v6.0.0)** and offers:

- **Mutation selection:** 1016G or 1534C  
- **Interactive filtering:** by year and region  
- **Site-level scatter maps:**  
  - Point color = mutation frequency  
  - Point size = number of genotyped individuals  
  - Black points = no mutation detected (frequency = 0)  
- **Province-level heatmaps:** aggregated frequencies (red gradient)  
- **Tooltip-rich interactivity:** number tested, frequency, location, data source  
- **Mapbox-based geographic context**

---

## Requirements

Core packages:
- Dash ≥ 3.0.4
- Plotly ≥ 6.0.0
- Pandas

---

## Licenses

**Code License:** MIT License (see `LICENSE`).

**Test Data License:** All test datasets in `/test_data` are released under CC0 1.0 Universal (Public Domain Dedication).
- GeoPandas
- Shapely
