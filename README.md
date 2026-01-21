# Air-Quality-Monitoring-Dashboard
This project is an interactive Air Quality Dashboard developed using Python Dash and Plotly to visualize and analyze air pollution levels across major cities in Sri Lanka. The dashboard enables users to explore air quality patterns, pollutant concentrations, seasonal variations, and alert conditions through dynamic visualizations.

##  Data Description

The dashboard uses **city-wise air quality datasets** stored as CSV files. Each dataset contains time-stamped measurements of multiple environmental indicators, including:

* PM10 (μg/m³)
* PM2.5 (μg/m³)
* Carbon Monoxide (μg/m³)
* Carbon Dioxide (ppm)
* Nitrogen Dioxide (μg/m³)
* Sulphur Dioxide (μg/m³)
* Dust (μg/m³)
* UV Index

Data is preprocessed by converting timestamps to date formats, calculating **daily averages**, and merging all cities into a single dataset for comparative analysis.

---

##  Dashboard Structure & Features

The application is organized into **three main tabs**, each designed to support different levels of analysis.

---

### Tab 1: Overview

Provides a **high-level summary of air quality conditions** for a selected city and month.

**Key features:**

* City and month selection using dropdown menus
* Summary cards displaying average pollutant levels
* Automatic air quality classification
  *(Good, Moderate, Unhealthy for Sensitive Groups, Unhealthy)* based on PM10, PM2.5, and CO thresholds
* Heatmap showing daily pollutant intensity over time
* Grouped bar chart visualizing daily pollutant trends

This tab helps users quickly understand the **overall air quality status** of a city.

---

###  Tab 2: City Trends

Focuses on **detailed pollutant behavior within a city** using two sub-tabs.

#### 🔹 Particulate Matter Concentration

* Line charts for **PM2.5 and PM10**
* Month-wise comparison using radio buttons
* Highlights short-term fluctuations and pollution peaks

#### 🔹 Pollutant Analysis

* Bar chart showing **maximum monthly pollutant levels**
* Pie chart representing **seasonal pollution contribution**
* Weekly **UV Index heatmap** to identify exposure patterns across days and weeks

This tab enables deeper insight into **seasonal and pollutant-specific trends**.

---

###  Tab 3: Air Quality Analysis

Designed for **comparative and analytical exploration** across cities.

**Includes:**

* Bar chart comparing average pollutant levels between cities
* Scatter plot to study **correlations between pollutants**
* Alert and outlier detection system using predefined thresholds
* Visual highlighting of cities exceeding safe air quality limits

This section supports **decision-making and risk identification**.

---

##  Alert & Classification Logic

The dashboard includes a rule-based air quality classification system:

* Uses PM10, PM2.5, and CO concentration thresholds
* Automatically assigns air quality status and color indicators
* Flags extreme pollution values as alerts for quick identification

---

##  Technologies Used

* **Python**
* **Dash** – Web application framework
* **Plotly Express & Graph Objects** – Interactive visualizations
* **Pandas** – Data preprocessing and aggregation

---

##  Use Cases

* Environmental monitoring and awareness
* Academic dashboard and data visualization projects
* Urban air quality comparison
* Identifying pollution hotspots and health risks

