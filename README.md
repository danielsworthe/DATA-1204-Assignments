# Assignment 3 & 4: Data Pipeline and Interactive Statistical Analysis  
**Pack B — Weather & Air Quality**

---

## Project Overview

This project is completed in two parts:

### **Assignment 3 (Part 1) — Data Engineering**
A data pipeline was built using two public APIs following a **Bronze → Silver → Gold** architecture:

- **Bronze:** Raw API data (JSON)
- **Silver:** Cleaned and structured datasets
- **Gold:** Final dataset prepared for statistical analysis

---

### **Assignment 4 (Part 2) — Statistical Analysis App**
The project was extended by:

- Adding a **new external data source (holidays)**
- Creating additional derived variables
- Building an **interactive statistical analysis app using Streamlit**
- Performing multiple statistical tests

---

## Data Sources

This project uses the following APIs:

- Weather Data: :contentReference[oaicite:0]{index=0}  
- Air Quality Data: :contentReference[oaicite:1]{index=1}  
- Holiday Data (Assignment 4): :contentReference[oaicite:2]{index=2}  

All datasets are aligned using the `date` field.

---

## Data Pipeline Architecture

### Bronze Layer (Raw Data)
- Raw JSON data collected from APIs
- Stored without modification
- Preserves original structure for traceability

---

### Silver Layer (Cleaned Data)
- JSON parsed into structured tables
- Key transformations:
  - Convert timestamps to `date`
  - Select relevant columns
  - Ensure correct data types
  - Aggregate hourly air quality → daily averages
  - Clean and structure holiday data

---

### Gold Layer (Final Dataset)

#### Assignment 3 Gold Dataset:
- Merged weather + air quality data
- Features:
  - `bad_weather_day`
  - `bad_air_day`

#### Assignment 4 Final Dataset:
- Added holiday data
- New features:
  - `is_holiday`
  - `holiday_name`
  - `day_type`

This final dataset is fully prepared for statistical analysis and visualization.

---

## Final Dataset Structure

| Column | Description |
|------|-------------|
| date | Observation date |
| temp_max | Maximum daily temperature |
| temp_min | Minimum daily temperature |
| precipitation | Daily precipitation |
| pm25 | Daily average PM2.5 |
| bad_weather_day | Indicator of poor weather |
| bad_air_day | Indicator of poor air quality |
| is_holiday | Indicator for holidays |
| holiday_name | Name of holiday |
| day_type | Holiday vs Non-holiday |

---

## Statistical Analysis

### Core Question:
Is air quality (PM2.5) affected by weather conditions and holidays?

---

### Tests Performed:

1. **One-Sample t-test**
   - Compare mean to benchmark value

2. **Two-Sample t-test**
   - Compare PM2.5 on holiday vs non-holiday days

3. **Chi-Square Test**
   - Relationship between holiday status and bad air days

4. **Variance Comparison (Levene’s Test)**
   - Compare variability between groups

5. **Correlation Analysis**
   - Relationship between temperature and PM2.5

---

## Interactive App

An interactive dashboard was built using :contentReference[oaicite:3]{index=3}.

### Features:
- Data filtering (date range, categories)
- Interactive visualizations:
  - Time series (PM2.5)
  - Histograms (temperature)
  - Boxplots (group comparisons)
  - Scatter plots (correlation)
- Statistical test outputs with interpretation
- Summary metrics

---

## How to Run the Project

### 1. Install Dependencies

pip install -r requirements.txt

---

### 2. Run Assignment 3 Pipeline

python ingest/ingest_weather.py
python ingest/ingest_air_quality.py

python transform/transform_weather.py
python transform/transform_air_quality.py

python transform/create_gold.py

---

### 3. Run Assignment 4 Pipeline

python ingest/ingest_holidays.py
python transform/transform_holidays.py
python transform/create_final_dataset.py

---

### 4. Launch the App

streamlit run app/streamlit_app.py

---

## 📁 Project Structure

assignment3&4/
│
├── data/
│ ├── bronze/
│ ├── silver/
│ └── gold/
│
├── ingest/
├── transform/
├── app/
│ └── streamlit_app.py
│
├── analysis_preview.md
├── assignment4_analysis_plan.md
├── assignment4_reflection.md
├── README.md
├── requirements.txt
└── .gitignore

---

## AI Usage

### Tools Used
- ChatGPT  
- Gemini  

---

### How AI Helped
AI tools were used to:
- Design the data pipeline structure
- Generate and refine Python scripts
- Explain statistical concepts and test selection
- Debug and troubleshoot errors
- Validate and improve code accuracy

Gemini was especially useful for:
- Troubleshooting runtime errors
- Explaining ChatGPT-generated code
- Cross-verifying correctness
- Providing additional clarification

---

### Example of Verification / Fix
While executing `transform/transform_weather.py`, Windows 11 Smart App Control blocked part of the application.

Using Gemini:
- I learned what Smart App Control is
- Received guidance on how to resolve the issue
- Followed suggested steps (including system adjustments and restart)

After restarting, the script executed successfully.

This demonstrates independent problem-solving and verification beyond AI-generated solutions.

---

## Notes

- This project is designed for learning purposes, not production use
- Data is limited to a selected time period
- Statistical tests assume independence and reasonable distributions
- Correlation does not imply causation

---

## Video Demonstration (Unavailable on GitHub)

A video demonstration accompanies this project and includes:

- Explanation of the data pipeline
- Walkthrough of the Streamlit app
- Demonstration of statistical tests
- Explanation of the added data source
- Discussion of challenges and limitations

---

## Conclusion

This project demonstrates:

- Building a complete data pipeline  
- Integrating multiple data sources  
- Preparing data for statistical analysis  
- Developing an interactive analytics application  

The final result is a structured, interpretable dataset and a functional app that supports real-world analytical thinking.

---