# High-Risk-Analytics-Data-Science-Project
Chicago Crash Ranking Dashboard
Overview

This Streamlit application provides an interactive ranking tool for analyzing traffic crash data in Chicago. Users can filter crashes by time range, damage level, injury severity, lighting conditions, and cause type, then view ranked crash hotspots by street or by approximate 50-meter grid. The goal is to identify the most frequent and dangerous crash locations using publicly available data.

Features

Ranking Modes

Most Frequent Crash Locations

Most Frequent (Weighted by Injury Severity)

Most Dangerous Crash Locations

Filter Options

Date range

Damage level

Crash type

Injury severity (non-incapacitating, incapacitating, fatal)

Primary cause (user error, non-user error, vehicle error)

Lighting conditions

Aggregation

Results can be grouped by street or by location grid (approximately 50 meters).

Metrics are calculated on a per-year basis across a nine-year dataset.

Data

The app uses a dataset named Newnew_dataset.csv.
Required columns include:

LATITUDE, LONGITUDE, CRASH_DATE_ONLY, DAMAGE, CRASH_TYPE,
INJURIES_FATAL, INJURIES_INCAPACITATING, INJURIES_NON_INCAPACITATING,
PRIMARY_CONTRIBUTORY_CAUSE, LIGHTING_CONDITION, STREET_NAME, INJURY_SCORE

How to Run

Install dependencies:

pip install streamlit pandas plotly


Launch the app:

streamlit run st_ranking.py


Open your browser at http://localhost:8501

Next Steps

Add a heatmap visualization to display crash density across Chicago.

Implement map-based interactivity (zoom, hover details, and filter overlays).

Optimize performance for larger datasets.
