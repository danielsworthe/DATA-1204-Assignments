from pathlib import Path
from scipy import stats
from textwrap import dedent 
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

DATA_PATH = Path("data/gold/final_dataset.csv")

st.set_page_config(
    page_title="Toronto 2025 Weather & Air Quality Analysis",
    page_icon="🌦️",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Could not find {DATA_PATH}. Run the transformation scripts first."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    # Safety fallback if a few columns are missing
    if "bad_air_day" not in df.columns and "pm25" in df.columns:
        df["bad_air_day"] = (df["pm25"] > 35).astype(int)

    if "bad_weather_day" not in df.columns and {"precipitation", "temp_max"}.issubset(df.columns):
        df["bad_weather_day"] = (
            (df["precipitation"] > 5) | (df["temp_max"] < 0)
        ).astype(int)

    if "is_holiday" in df.columns:
        df["is_holiday"] = df["is_holiday"].fillna(0).astype(int)
    else:
        df["is_holiday"] = 0

    if "holiday_name" in df.columns:
        df["holiday_name"] = df["holiday_name"].fillna("N/A")
    else:
        df["holiday_name"] = "N/A"

    df["day_type"] = np.where(df["is_holiday"] == 1, "Holiday", "Non-holiday")

    return df


def result_text(p_value: float) -> str:
    return "Reject H₀" if p_value < 0.05 else "Fail to reject H₀"


def safe_number(x) -> str:
    try:
        return f"{float(x):.4f}"
    except Exception:
        return "N/A"


try:
    df = load_data()
except Exception as e:
    st.error(str(e))
    st.stop()

st.title("Weather & Air Quality Interactive Statistical Analysis")
st.subheader("Toronto 2025")
st.caption("Durham College — Applied Data Analytics — DATA 1204 — Assignment 4 — Streamlit App")

st.subheader("Project Overview")
st.write(
    """
    This dashboard was made for my Statistical and Predictive Modelling for Analytics 1 (DATA 1204) course in the Applied Data Analytics 
    program at Durham College. This is the fourth assignment in my DATA 1204 course and is a continuation of Assignment 3: Data Pipeline for Statistical Analysis. 
    In the previous assignment, I made a project analysing weather and air-quality data in Toronto in 2025.  
    This was done using a medallion architecture (bronze-silver-gold) data design pattern for simple data engineering. 
    I added a new external data source for this assignment. That being a Canadian/Ontario holiday calendar from a public API. 
    The join key that I used was 'date' to join my original gold-level dataset to the data from the new API. The addition of 
    this new data source gives us a useful categorical comparison: holiday days versus non-holiday days. The main question 
    that this project explores is "Do holidays affect air quality patterns?" and related questions.
    
    HINT: July has the most bad air days.
    """
)

with st.sidebar:

    st.header("Filters")
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    st.caption("Data Preview tab")

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    st.caption("Visual Story tab")

    view_filter = st.selectbox(
        "Filter Charts",
        ["All rows", "Holiday only", "Non-holiday only"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### Test Settings")
    st.caption("Hypothesis Tests tab")
    one_sample_var = st.selectbox(
        "Variable for one-sample t-test",
        ["pm25", "temp_max", "temp_min", "precipitation"],
        index=0,
    )
    benchmark = st.number_input("Benchmark value", value=35.0, step=1.0)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.warning("Please select both a start date and an end date to filter the data.")
    st.stop()
analysis_df = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)].copy()

chart_df = analysis_df.copy()
if view_filter == "Holiday only":
    chart_df = chart_df[chart_df["is_holiday"] == 1]
elif view_filter == "Non-holiday only":
    chart_df = chart_df[chart_df["is_holiday"] == 0]

chart_df = chart_df.sort_values("date")

# Calculating values for dynamic colour changes
avg_pm25 = analysis_df["pm25"].mean()
bad_air_count = int(analysis_df["bad_air_day"].sum())
total_days = len(analysis_df)
bad_air_ratio = bad_air_count / total_days if total_days > 0 else 0

def air_quality_level(avg_pm25, bad_air_ratio):
    """
    Returns a clearer colour/status pair.
    """
    # PM2.5 average status
    if avg_pm25 < 12.0:
        pm_color = "green"
        pm_status = "Good"
    elif avg_pm25 < 35.4:
        pm_color = "orange"
        pm_status = "Moderate"
    else:
        pm_color = "red"
        pm_status = "Unhealthy"

    # Bad-air-day status
    # Wider bands so orange and red are easier to distinguish
    is_full_year = (start_date == min_date) and (end_date == max_date)

    if is_full_year:
        air_color = "red"
        air_status = "Full Year Selected"
    elif bad_air_count == 0:
        air_color = "green"
        air_status = "No Pollution Days"
    elif bad_air_count == 1:
        air_color = "orange"
        air_status = "One Pollution Day"
    else:
        air_color = "red"
        air_status = "Multiple Pollution Days"

    return pm_color, pm_status, air_color, air_status

pm_color, pm_status, air_color, air_status = air_quality_level(avg_pm25, bad_air_ratio)

# Display
st.write("---")
col1, col2, col3, col4 = st.columns(4)

from textwrap import dedent

def status_card(label, value, status, color):
    color_map = {
        "green": {"bg": "#d4edda", "border": "#198754", "text": "#198754"},
        "orange": {"bg": "#fff3cd", "border": "#fd7e14", "text": "#fd7e14"},
        "red": {"bg": "#ffcccc", "border": "#cc0000", "text": "#b30000"},
        "gray": {"bg": "#f1f3f5", "border": "#ced4da", "text": "#000000"},
    }

    c = color_map[color]

    html = dedent(f"""
    <div style="background-color: {c['bg']}; border: 1px solid {c['border']}; border-radius: 12px; padding: 14px; text-align: center;">
        <div style="font-size: 14px; font-weight: 600; color: #333;">{label}</div>
        <div style="font-size: 30px; font-weight: 700; color: {c['text']};">{value}</div>
        <div style="font-size: 13px; color: #333;">{status}</div>
    </div>
    """)

    st.markdown(html, unsafe_allow_html=True)

with col1:
    status_card("Rows in Data", f"{total_days:,}", "Filtered Period", "gray")

with col2:
    status_card("Average PM2.5", f"{avg_pm25:.1f}", f"Status: {pm_status}", pm_color)

with col3:
    holiday_count = int(analysis_df["is_holiday"].sum())
    holiday_color = "green" if holiday_count > 0 else "gray"
    holiday_status = "Holiday Dates Included" if holiday_count > 0 else "No Holidays in Range"
    status_card("Holiday Days", f"{holiday_count}", holiday_status, holiday_color)

with col4:
    status_card("Bad Air Days", f"{bad_air_count}", f"Trend: {air_status}", air_color)

st.write("---")

tab1, tab2, tab3, tab4 = st.tabs(["Data Preview", "Visual Story", "Hypothesis Tests", "Reflection"])

with tab1:
    st.subheader("Data Preview")
    st.write("Sample of the final dataset (first 10 rows):")
    st.dataframe(analysis_df.head(10), column_config={"date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"), 
    "province": None, "federal_holiday": None, "is_holiday": st.column_config.CheckboxColumn("is_holiday")}, 
    width='stretch', hide_index=True,)

    st.write("Summary statistics for numeric columns:")
    st.dataframe(analysis_df.describe(include=[np.number]).T, width='stretch')

    st.write("Useful columns in this project:")

    column_info = pd.DataFrame({
        "Column": [
            "pm25",
            "temp_max",
            "precipitation",
            "bad_air_day",
            "bad_weather_day",
            "is_holiday",
            "day_type"
        ],

        "Description": [
            "Daily average PM2.5 air pollution level (accumulation of fine particles measuring 2.5 micrometers or smaller)",
            "Daily maximum temperature",
            "Daily precipitation total",
            "Indicates whether daily PM2.5 exceeded 35 µg/m³ (exceeded the pollution threshold)",
            "Indicates days with heavy precipitation (>5mm) or freezing temperatures (maximum temperature below 0°C)",
            "Binary (yes or no) holiday indicator from the Canadian Holiday API",
            "Categorical label: Holiday or Non-holiday"
        ]
    })

    st.dataframe(
        column_info,
        width='stretch',
        hide_index=True
    )

with tab2:
    st.subheader("Visual story")

    st.info(f"Current chart filter: {view_filter}")
    left, right = st.columns(2)
    with left:
        fig1 = px.line(
            chart_df,
            x="date",
            y="pm25",
            title="PM2.5 Over Time",
            labels={"pm25": "PM2.5", "date": "Date"},
        )
        st.plotly_chart(fig1, width='stretch')

    with right:
        fig2 = px.histogram(
            chart_df,
            x="temp_max",
            nbins=30,
            title="Distribution of Daily Maximum Temperature",
            labels={"temp_max": "Daily Max Temperature"},
        )
        st.plotly_chart(fig2, width='stretch')

    left2, right2 = st.columns(2)
    with left2:
        fig3 = px.box(
            chart_df,
            x="day_type",
            y="pm25",
            title="PM2.5 by Holiday / Non-holiday Days",
            labels={"day_type": "Day Type", "pm25": "PM2.5"},
        )
        st.plotly_chart(fig3, width='stretch')

    with right2:
        fig4 = px.scatter(
            chart_df,
            x="temp_max",
            y="pm25",
            color="day_type",
            title="Temperature vs PM2.5",
            labels={"temp_max": "Daily Max Temperature", "pm25": "PM2.5"},
        )
        st.plotly_chart(fig4, width='stretch')

with tab3:
    st.subheader("Hypothesis tests")

    st.markdown("### 1) One-sample t-test")
    one_sample_data = analysis_df[one_sample_var].dropna()

    st.write(f"Variable: `{one_sample_var}`")
    st.write(f"Null hypothesis: mean of `{one_sample_var}` = {benchmark}")
    st.write(f"Alternative hypothesis: mean of `{one_sample_var}` ≠ {benchmark}")

    if len(one_sample_data) >= 2:
        t_stat, p_val = stats.ttest_1samp(one_sample_data, popmean=benchmark)
        st.write(f"t-statistic: **{safe_number(t_stat)}**")
        st.write(f"p-value: **{safe_number(p_val)}**")
        st.write(f"Decision: **{result_text(p_val)}**")
    else:
        st.warning("Not enough rows for the one-sample t-test after filtering. Filter Date Range to select more/alternate dates.")

    st.markdown("---")
    st.markdown("### 2) Two-sample t-test")
    holiday_pm25 = analysis_df.loc[analysis_df["is_holiday"] == 1, "pm25"].dropna()
    nonholiday_pm25 = analysis_df.loc[analysis_df["is_holiday"] == 0, "pm25"].dropna()

    st.write("Variable: `pm25`")
    st.write("Groups: holiday days vs non-holiday days")
    st.write("Null hypothesis: the two group means are equal")
    st.write("Alternative hypothesis: the two group means are different")

    if len(holiday_pm25) >= 2 and len(nonholiday_pm25) >= 2:
        t_stat2, p_val2 = stats.ttest_ind(
            holiday_pm25,
            nonholiday_pm25,
            equal_var=False,  # Welch's t-test
            nan_policy="omit",
        )
        st.write(f"t-statistic: **{safe_number(t_stat2)}**")
        st.write(f"p-value: **{safe_number(p_val2)}**")
        st.write(f"Decision: **{result_text(p_val2)}**")
    else:
        st.warning("Not enough rows in one of the groups for the two-sample t-test. Filter Date Range to select more/alternate dates.")

    st.markdown("---")
    st.markdown("### 3) Chi-square Test of Independence")
    chi_df = analysis_df.copy()
    chi_df["bad_air_label"] = np.where(chi_df["bad_air_day"] == 1, "Bad air day", "Normal air day")

    contingency = pd.crosstab(chi_df["day_type"], chi_df["bad_air_label"])

    st.write("Question: Are holiday days independent of bad air days?")
    st.dataframe(contingency, width='stretch')

    if contingency.shape[0] >= 2 and contingency.shape[1] >= 2:
        chi2, chi_p, dof, expected = stats.chi2_contingency(contingency)
        st.write(f"Chi-square statistic: **{safe_number(chi2)}**")
        st.write(f"Degrees of freedom: **{dof}**")
        st.write(f"p-value: **{safe_number(chi_p)}**")
        st.write(f"Decision: **{result_text(chi_p)}**")
    else:
        st.warning("Not enough categories for the chi-square test. Filter Date Range to select more/alternate dates.")

    st.markdown("---")
    st.markdown("### 4) Variance Comparison")
    st.write("Method: Levene test for equality of variance")
    st.write("Question: Is the spread of PM2.5 different on holiday and non-holiday days?")

    if len(holiday_pm25) >= 2 and len(nonholiday_pm25) >= 2:
        lev_stat, lev_p = stats.levene(holiday_pm25, nonholiday_pm25, center="median")
        st.write(f"Levene statistic: **{safe_number(lev_stat)}**")
        st.write(f"p-value: **{safe_number(lev_p)}**")
        st.write(f"Decision: **{result_text(lev_p)}**")
    else:
        st.warning("Not enough rows for the variance comparison. Filter Date Range to select more/alternate dates.")

    st.markdown("---")
    st.markdown("### 5) Correlation Analysis")
    corr_method = st.selectbox("Correlation method", ["Pearson", "Spearman"], index=1)

    corr_df = analysis_df[["temp_max", "pm25"]].dropna()

    if len(corr_df) >= 2:
        if corr_method == "Pearson":
            corr_value, corr_p = stats.pearsonr(corr_df["temp_max"], corr_df["pm25"])
        else:
            corr_value, corr_p = stats.spearmanr(corr_df["temp_max"], corr_df["pm25"])

        st.write("Variables: `temp_max` and `pm25`")
        st.write(f"{corr_method} correlation: **{safe_number(corr_value)}**")
        st.write(f"p-value: **{safe_number(corr_p)}**")
        st.write(f"Decision: **{result_text(corr_p)}**")
    else:
        st.warning("Not enough rows for correlation analysis. Filter Date Range to select more/alternate dates.")

with tab4:
    st.subheader("Reflection / Limitations")
    st.markdown(
        """
        - The app uses a local Gold dataset (available on GitHub), so it is easy to run and explain.
        - The holiday source gives a simple, meaningful grouping variable.
        - One-sample t-tests need a benchmark that you can justify clearly.
        - The t-tests assume independence and roughly normal sampling behavior.
        - The chi-square test needs reasonable expected cell counts.
        - The correlation result shows association, not causation.
        - Exact date joining can miss any real-world effects that happen before or after the observed holiday date.
        - Analysis is restricted to a historical one-year (2025) dataset. Meaning the pipeline is currently optimized for batch processing rather than live API polling.
        """
    )

print("Full file executed successfully.")