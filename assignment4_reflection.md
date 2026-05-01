# Assignment 4 Reflection

## What Worked Well
The holiday calendar joined cleanly to the Assignment 3 Gold dataset using the date field. That made it easy to create a clear story about holiday versus non-holiday days and how they relate to PM2.5 and weather conditions.

## What Was Difficult
The hardest part was deciding on a benchmark for the one-sample t-test and making sure the holiday source added something meaningful instead of just adding extra columns. I also had to think carefully about observed holiday date versus literal holiday date.

## Assumptions That Were Hardest to Defend
The t-tests assume roughly independent observations and reasonable sampling behavior. The chi-square test requires expected counts that are not too small. The correlation result should be interpreted as association, not causation.

## What I Would Improve
If this project became a larger analytics product, I would add a second external source such as traffic, mobility, wildfire-smoke, or even energy demand data. That would create a stronger story and possibly improve the analysis beyond a simple holiday comparison. I could even add another city to compare Toronto with, such as Montreal for example, by remaking my initial data pipeline and statistical analysis for that city.