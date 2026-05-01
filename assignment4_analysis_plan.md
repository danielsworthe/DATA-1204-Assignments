# Assignment 4 Analysis Plan

## 1. New source added
I added the Canada Holidays API for Ontario. This source provides holiday dates and holiday names, which are joined to the Weather & Air Quality Gold dataset by date.

## 2. Join key
The join key is `date`. In the holiday Silver table, I use the observed holiday date as the daily date so that it lines up with the weather and air-quality observations.

## 3. New variables created
These are:
- `is_holiday`
- `holiday_name`
- `day_type`
- `federal_holiday`

## 4. Story / question
My dashboard asks whether holiday days are associated with different air-quality patterns and whether PM2.5 behaves differently on holiday days compared to non-holiday days.

## 5. Required analyses
1. **One-sample t-test**
   - Question: Is mean PM2.5 different from a benchmark value?
2. **Two-sample t-test**
   - Question: Is mean PM2.5 different on holiday days versus non-holiday days?
3. **Chi-square test of independence**
   - Question: Are holiday days independent of bad-air days?
4. **Variance comparison**
   - Question: Is PM2.5 variance different on holiday days versus non-holiday days?
5. **Correlation analysis**
   - Question: Is temperature associated with PM2.5?

## 6. Visuals that support the analyses
These include:
- Line chart of PM2.5 over time
- Histogram of daily maximum temperature
- Box plot of PM2.5 by holiday / non-holiday day
- Scatter plot of temperature vs PM2.5

## 7. Why these methods fit
- The one-sample t-test compares one numeric sample against a fixed benchmark.
- The two-sample t-test compares the means of two groups.
- The chi-square test is appropriate for two categorical variables.
- The variance comparison checks whether spread differs between groups.
- Correlation measures the relationship between two quantitative variables.