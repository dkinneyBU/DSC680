---
layout: post
title:  "Exoplanet Prediction"
author: David Kinney
categories: [ projects, exoplanets ]
image: ../images/ExoplanetTypes.png
description: "Are we alone?"
---
## Are we alone?

> Whether life exists beyond Earth is one of the most profound questions of all time. The answer will change us forever, whether it reveals a universe rich with life, one in which life is rare and fragile, or even a universe in which we can find no other life at all.  

Source: https://exoplanets.nasa.gov/what-is-an-exoplanet/overview/


For this project, I attempt to see if I can train a Machine Learning model to predict whether or not an astral object might be an exoplanet.  

[![](https://img.shields.io/badge/Word-white paper-2B579A?logo=Microsoft Word)](https://dkinneyBU.github.io/papers/Predicting Exoplanets.docx)

[![](https://img.shields.io/badge/PowerPoint-Presentation-B7472A?logo=Microsoft PowerPoint)](https://dkinneyBU.github.io/presentations/Climate Change.pptx)


![image](https://user-images.githubusercontent.com/43932354/120625299-8f342b80-c42f-11eb-891c-7a82cbd4319a.png)  

Image credit: NASA/JPL-Caltech/Lizbeth B. De La Torre  

Exoplanets are planets that orbit around a star, as in our solar system. These bodies are very hard to see directly with telescopes since they are hidden by the bright glare of the stars they orbit. The Kepler Objects of Interest (KOI) dataset contains various measurements of transit, in addition to many others that aid in identifying exoplanets. In 2009, NASA launched the Kepler spacecraft to search for exoplanets. Kepler looked for planets in a wide range of sizes and orbits that circled around stars of varied size and temperature. [2] The Kepler spacecraft detected exoplanets using the transit method. As a planet passes (transits) in front of a star, it blocks out a bit of the star’s light. By observing the stars’ change in brightness astronomers can figure out the size of the orbiting planet as well as how far away it is from the star. Further, this data then aids in calculating the planet’s temperature, and the chances that it may contain liquid water—*the stuff of life*…  

![image](https://user-images.githubusercontent.com/43932354/120625646-ea661e00-c42f-11eb-86d4-5b6e96986169.png)  
Source: https://spaceplace.nasa.gov/all-about-exoplanets/en/


The  [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/index.html) is an online astronomical exoplanet and stellar catalog and data service that collates and cross-correlates astronomical data and information on exoplanets and their host stars. As this data is used by astronomers to arrive at whether an object is an exoplanet, it follows that it is likely a Machine Learning model can be developed to make predictions based on the same data.  

#### Modeling ####

A baseline model was established by training a `Random Forest Classifier`, randomly assigning 1,000 estimators. The function containing the model also applied a `StandardScaler` to standardize the data prior to model fitting. This resulted in an accuracy score of 86%.  

Measure | Precision | Recall | F1 score | Support
------- |---------- | ------ | -------- | -------
Candidate | 0.78 | 0.66 | 0.71 | 601
Confirmed | 0.86 | 0.87 | 0.87 | 600
False Positive | 0.89 | 0.96 | 0.93 | 1190
Accuracy |  |  | 0.86 | 2391 
Macro avg | 0.85 | 0.83 | 0.84 | 2391
Weighted avg | 0.86 | 0.86 | 0.86 | 2391  


Actual | Predicted Candidate | Predicted Confirmed | Predicted False Positive
------ | ------------------- | ------------------- | ------------------------
Candidate | 1104 | 289 | 372
Confirmed | 198 | 1517 | 43
False Positive | 163 | 7 | 3480  

![image](https://user-images.githubusercontent.com/43932354/120625775-036ecf00-c430-11eb-80a4-c8cc2944d370.png)

This was followed by performing a randomized search by leveraging a `RandomizedSearchCV model` selector. Interestingly, this did not result in an improvement in accuracy.  

The eight categorical variables that were dropped were either informational (url paths, transit model used) or were predominately one value. As an example, “fittype” was one of three values, such as Least Mean Squares. Roughly 90% of the values in this observation were the same value. A `StandardScaler` was employed rather than a min/max scaler (normalization). Standardization does not bind the variables to a specific range, and some of the variables had an extreme range. As one example,  the minimum value for `koi_period` was .24, and the maximum value was 129,995. I did look at these extreme values and decided they were valid for predicting false positives; therefore I did not want to exclude them. Standardization is much less affected by outliers. I originally had hoped to train a model on the subsets based on categories, but ran out of time. I feel this is still worth pursuing. If one of the subsets results in better accuracy than the the entire subset, less observational data will be required to predict object disposition. Lastly, other models were evaluated (`SVM, AdaBoost, XGBoost, TPOT`) but the original `Random Forest Classifier` still resulted in the best results.    

#### Conclusions ####

While 86% accuracy is not exemplary, that was achieved with a simple baseline model. I am confident greater accuracy is possible, either by fine-tuning the hyperparameters for the Random Forest Classifier, or by training against a larger dataset, if one becomes available. Given that Machine Learning algorithms can process data faster than humans by an order of magnitude, deployment of such a model that can classify observations of the trillions of solar objects present in the observable universe with blinding speed will free up astronomers for more creative endeavors; one area where humans still dominate.

**References**  

[1] NASA Exoplanet Archive – NASA Exoplanet Science Institute https://exoplanetarchive.ipac.caltech.edu/index.html  
[2] What Is an Exoplanet? | NASA Space Place – NASA Science for Kids  
[3] Overview | What is an Exoplanet? – Exoplanet Exploration: Planets Beyond our Solar System (nasa.gov)  

![image](https://user-images.githubusercontent.com/43932354/120625890-1aadbc80-c430-11eb-8b00-b12d008c278f.png)
