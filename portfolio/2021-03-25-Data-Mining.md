---
layout: post
title:  "Data Mining"
author: David Kinney
categories: [ projects, LSI ]
image: ../images/datamining.png
description: ""
---
## Mining the Life Satisfaction Index

The central point of this dataset is the so-called, **“Life Satisfaction Index”.** In other words, do indicators in the categories of housing, income, jobs, community, education, environment, civic engagement, health, etc. really lead to a better, more satisfied life? Let’s focus on a few high-level categories to see how the indicators correlate with the LSI. . .  

* **Wealth** Net Wealth, Labor Market Insecurity, Employment rate  
* **Environment** Air pollution, Homicide rate, Water quality  
* **Health** Life expectancy, Self-reported health, Long work hours  

There does not seem to be any noticeable normal distribution amongst any of the indicators, although some–such as HS_LEB (Life Expectancy) exhibit normal-ish distribution on a
skewed scale.  

* **Wealth** - somewhat surprisingly, Net Wealth does not appear to be as important as labor market security and the employment rate. Having said that, removing the data points above $500,000 might tell a different story.  
* **Environment** - Air and water quality seem to factor higher than the homicide rate, which shows almost no effect on the LSI.  
* **Health** - Life expectancy seems like an obvious factor, but I was also satisfied to see long work hours affect the index as well.

My repo for this project can be found [here](https://github.com/dkinneyBU/data-mining).
