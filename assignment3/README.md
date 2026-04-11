# Assignment 3: Data Pipeline for Statistical Analysis  
**Pack B — Weather & Air Quality**

## Project Overview
This project builds a simple data pipeline using two public APIs to prepare a dataset for statistical analysis. The pipeline follows a **Bronze → Silver → Gold** architecture:

- **Bronze:** Raw data collected from APIs  
- **Silver:** Cleaned and structured data  
- **Gold:** Final dataset prepared for statistical testing  

The goal is to design a dataset that can support hypothesis testing in a later stage of the assignment.

---

## Data Sources

This project uses the following APIs:

- Weather Data: :contentReference[oaicite:0]{index=0}  
- Air Quality Data: :contentReference[oaicite:1]{index=1}  

Both datasets are based on the same geographic location and time period, allowing for a clean join using the `date` field.

---

## Data Pipeline Architecture

### Bronze Layer (Raw Data)
- Data is collected directly from APIs and stored as raw JSON files.
- No modifications are made to preserve original data integrity.

### Silver Layer (Cleaned Data)
- JSON data is parsed and transformed into structured tables.
- Key steps:
  - Convert timestamps to `date`
  - Select relevant columns
  - Ensure proper data types
  - Aggregate hourly air quality data into daily averages

### Gold Layer (Final Dataset)
- Weather and air quality datasets are merged on `date`.
- Additional features are created:
  - `bad_weather_day` (precipitation > 5 OR temperature < 0)
  - `bad_air_day` (PM2.5 > 35)

This dataset is optimized for statistical analysis.

---

## Final Dataset Structure

| Column | Description |
|------|-------------|
| date | Observation date |
| temp_max | Maximum daily temperature |
| temp_min | Minimum daily temperature |
| precipitation | Daily precipitation total |
| pm25 | Daily average PM2.5 |
| bad_weather_day | Boolean indicator of poor weather |
| bad_air_day | Boolean indicator of poor air quality |

---

## Planned Statistical Analysis

**Research Question:**  
Is average PM2.5 higher on bad weather days compared to normal days?

- **Outcome Variable:** PM2.5 (continuous)  
- **Grouping Variable:** Bad weather day (True/False)  
- **Test:** Two-sample t-test  

---

## How to Run the Project

### 1. Install Dependencies
pip install -r requirements.txt


### 2. Run Data Ingestion
python ingest/ingest_weather.py
python ingest/ingest_air_quality.py


### 3. Run Data Transformation
python transform/transform_weather.py
python transform/transform_air_quality.py


### 4. Create Gold Dataset
python transform/create_gold.py


### 5. Output Location
data/gold/weather_air_quality_gold.csv


---

## Project Structure
assignment3/
│
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
│
├── ingest/
├── transform/
├── notebooks/
│
├── README.md
├── analysis_preview.md
├── requirements.txt
└── .gitignore


---

## AI Usage

### Tools Used
- ChatGPT  
- Gemini  

### How AI Helped
AI tools were used to:
- Structure the data pipeline (Bronze → Silver → Gold)
- Generate and refine Python scripts for API ingestion and data transformation
- Debug errors and troubleshoot issues
- Explain concepts such as ETL pipelines and statistical test preparation
- Cross-check code for correctness and completeness

Gemini was particularly helpful for:
- Troubleshooting errors encountered during execution
- Explaining and validating ChatGPT-generated code
- Suggesting improvements and minor enhancements for accuracy
- Supporting deeper understanding of assignment requirements

### Example of Verification / Fix
While executing the `transform/transform_weather.py` script, Windows 11 Smart App Control blocked part of the application. I used Gemini to investigate the issue. It explained what Smart App Control is and provided guidance on how to resolve it, including referencing external resources. I followed the suggested steps (including checking system settings), and after restarting my computer, the issue was resolved and the script executed successfully.

This demonstrates that while AI tools provided guidance, I independently verified and resolved issues to ensure proper functionality.

---

## Notes
- The pipeline is designed for clarity and simplicity, not production use
- Data is limited to a selected time range for demonstration purposes
- The Gold dataset is intentionally structured for statistical analysis in the next phase of the assignment

---

## Conclusion
This project demonstrates how to:
- Collect data from APIs  
- Build a structured data pipeline  
- Prepare a dataset for statistical analysis  

The final dataset is clean, interpretable, and ready for hypothesis testing.

---