# Statistical Analysis Preview

**1.** 
Is average PM2.5 (fine airborne particles measuring 2.5 micrometers or less in width) higher on bad weather days compared to normal days?

**2.**
My outcome variable is the aformentioned PM2.5 as the continuous metric.

**3.**
My grouping variable is the calculated column, Bad weather day, as a true/false datatype.

**4.**
My binary (true/false) variable is the calculated column, Bad air day. This was defined as when PM2.5 > 35 (exceeding 35 micrograms per cubic meter of air, indicating unhealthy air quality). 

**5.**
The null hypothesis (H sub 0) that I might test is whether or not the Mean/average PM2.5 is the same on bad and normal weather days. The alternative hypothesis (H sub 1) that I might test is the assumption that Mean/average PM2.5 is higher on bad weather days.

**6.**
I think that the Two-sample or paired t-test fits best for this final dataset. This is because I have one continuous column () and one grouping column (bad_weather_day).