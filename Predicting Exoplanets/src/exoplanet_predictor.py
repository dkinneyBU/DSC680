# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 15:45:10 2021

@author: David
"""
# %% Import libraries
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
import seaborn as sns
import pandas as pd
from pandas_profiling import ProfileReport
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split, \
                                    cross_val_score, \
                                    cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import confusion_matrix, \
                                    accuracy_score, \
                                    precision_score, \
                                    recall_score, \
                                    classification_report
from tpot import TPOTClassifier

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# %% function definitions
def pca(df):
    
    # standardize the features matrix
    features = StandardScaler().fit_transform(df)
    
    # Create a PCA that retains 99% of the variance
    pca = PCA(n_components = 0.95)
    features_pca = pca.fit_transform(features)
    
    return features, features_pca


def plot_cm(cm):
    # plot confusion matrix
    fig, ax = plt.subplots(figsize = (10,8))
    
    sns.heatmap(conf_matrix_rf/np.sum(conf_matrix_rf), annot=True, 
                fmt='.2%', cmap='Blues', annot_kws={'size':15})
    
    ax.set_title('Random Forest Confusion Matrix', fontsize = 18, loc='left')
    
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize = 12)
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize = 12)
    
    plt.show()
    
# %% read df_final
# Read the Kepler Objects of Interest (KOI) df_final and look at one observation
df_koi = pd.read_csv('../DSC680/Predicting Exoplanets/data/cumulative_2021.03.16_17.10.21.csv')
print(df_koi.shape)
print(df_koi[1:2].T)

# %% clean data
# Remove variables with no data
df_koi_cleaned = df_koi.dropna(axis=1, how='all')

# Remove columns containing only zero
df_koi_cleaned = df_koi_cleaned.loc[:, (df_koi_cleaned != 0).any(axis=0)]

# Remove the err columns
df_koi_cleaned = df_koi_cleaned[df_koi_cleaned.columns.drop(
    list(df_koi_cleaned.filter(regex='_err')))]

# Still some variables that are all 0.0; will just drop them manually...
cols = ['koi_eccen','koi_ldm_coeff4','koi_ldm_coeff3']
df_koi_cleaned = df_koi_cleaned.drop(cols,axis=1)

df_koi_cleaned.shape
# %% describe
df_describe = pd.DataFrame(df_koi_cleaned.describe())
# print(df_describe)

# %% create subsets
# transit_columns = ['koi_period', 'koi_time0bk', 'koi_time0', 'koi_impact', 
#                    'koi_duration', 'koi_depth', 'koi_ror', 'koi_srho', 'koi_fittype', 
#                    'koi_prad', 'koi_sma', 'koi_incl', 'koi_teq', 'koi_insol', 'koi_dor', 
#                    'koi_limbdark_mod', 'koi_ldm_coeff2', 'koi_ldm_coeff1', 'koi_parm_prov']
# tce_columns = ['koi_max_sngle_ev', 'koi_max_mult_ev', 'koi_model_snr', 'koi_count', 
#                'koi_num_transits', 'koi_tce_plnt_num', 'koi_tce_delivname', 'koi_quarters', 
#                'koi_trans_mod', 'koi_datalink_dvr', 'koi_datalink_dvs']
# stellar_columns = ['koi_steff', 'koi_slogg', 'koi_smet', 'koi_srad', 'koi_smass', 'koi_sparprov']
# kic_columns = ['ra', 'dec', 'koi_kepmag', 'koi_gmag', 'koi_rmag', 'koi_imag', 'koi_zmag', 
#                'koi_jmag', 'koi_hmag', 'koi_kmag']
# pixel_columns = ['koi_fwm_sra', 'koi_fwm_sdec', 'koi_fwm_srao', 'koi_fwm_sdeco', 'koi_fwm_prao', 
#                  'koi_fwm_pdeco', 'koi_fwm_stat_sig', 'koi_dicco_mra', 'koi_dicco_mdec', 
#                  'koi_dicco_msky', 'koi_dikco_mra', 'koi_dikco_mdec', 'koi_dikco_msky']


# df_transit = df_koi_cleaned[transit_columns]
# df_tce = df_koi_cleaned[tce_columns]
# df_stellar = df_koi_cleaned[stellar_columns]
# df_kic = df_koi_cleaned[kic_columns]
# df_pixel = df_koi_cleaned[pixel_columns]

# %% pandas profiling
# Suppress SettingWithCopyWarning message generated by pandas-profiling
import warnings
warnings.simplefilter(action='ignore')

# profile = ProfileReport(df_koi_cleaned, title="Pandas Profiling Report")
# # profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
# pfile = "profile_report_{}.html".format(datetime.now().strftime('%m%d%y%H%M'))
# profile.to_file(pfile)
# %% prepare data
"""
Remove all descriptive variables to further simplify the df_final
In the interest of time, remove all categorical variables
"""
remove_cols = ['rowid', 'kepid', 'kepoi_name', 'kepler_name', 'koi_vet_stat',
               'koi_vet_date', 'koi_pdisposition', 'koi_fpflag_nt',
               'koi_fpflag_ss', 'koi_fpflag_co', 'koi_fpflag_ec', 'koi_disp_prov',
               'koi_comment', 'koi_limbdark_mod', 'koi_parm_prov', 'koi_tce_delivname',
               'koi_trans_mod', 'koi_trans_mod', 'koi_datalink_dvr', 'koi_datalink_dvs',
               'koi_sparprov', 'koi_fittype']
df_final = df_koi_cleaned.drop(remove_cols, axis=1)

# Separate labels from features
labels = df_final['koi_disposition']
df_features = df_final.drop(['koi_disposition'], axis=1)

# Replace missing numerical values with the median
imputer = SimpleImputer(strategy="median")
imputer.fit(df_features)
X = imputer.transform(df_features)
df_final = pd.DataFrame(X, columns=df_features.columns, index=df_features.index)

# %% Dimensionality Reduction
features, features_pca = pca(df_final)
print('Original number of features: {}'.format(features.shape[1]))
print('Reduced number of features: {}'.format(features_pca.shape[1]))

df_final = pd.DataFrame(df_final, columns=df_final.columns, index=df_final.index)

# %% correlation matrix
rcParams['figure.figsize'] = 20, 14
plt.matshow(df_final.corr())
plt.yticks(np.arange(df_final.shape[1]), df_final.columns)
plt.xticks(np.arange(df_final.shape[1]), df_final.columns)
plt.colorbar()

# %% train and test sets
# labels = np.array(labels)

train_features, test_features, train_labels, test_labels = train_test_split(
    df_final, labels, test_size = 0.25, random_state = 42)

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)
print('Training distribution: ',train_labels.value_counts(normalize=True))
print('Test distribution: ',test_labels.value_counts(normalize=True))

# %% train baseline model
# Instantiate model with 1000 decision trees
rf = RandomForestClassifier(n_estimators = 1000, random_state = 42)
rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)
print("Accuracy score: ", accuracy_score(test_labels, predictions))
print("Recall score: ", recall_score(test_labels, predictions, average=None))

cv_score = cross_val_score(rf, train_features, train_labels, cv=3, scoring='accuracy')
print("Cross validation score: ", cv_score)

print(classification_report(test_labels,predictions))

# %% confusion matrix
train_pred = cross_val_predict(rf, train_features,train_labels, cv=3)
conf_matrix_rf = confusion_matrix(train_labels, train_pred)
print(conf_matrix_rf)

plot_cm(conf_matrix_rf)

# %% randomized search
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 10)]

# Number of features to consider at every split
max_features = ['auto', 'sqrt']

# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)

# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]

# Method of selecting samples for training each tree
bootstrap = [True, False]

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

rf_2 = RandomForestClassifier(random_state = 42)

# Random search of parameters, using 3 fold cross validation, 
# search across 100 different combinations, and use all available cores

rf_random = RandomizedSearchCV(estimator = rf_2, 
                               param_distributions = random_grid, 
                               n_iter = 100, 
                               cv = 3, 
                               verbose=2, 
                               random_state=42, 
                               n_jobs = -1)
# Fit the random search model
rf_random.fit(train_features, train_labels)


# %% best params
# use these params for the next model
print(rf_random.best_params_)

# %% Model with Random Search CV Params
rf_rs = RandomForestClassifier(n_estimators = 522,
                               min_samples_split = 2,
                               min_samples_leaf = 2,
                               max_features = 'sqrt',
                               max_depth = 110,
                               bootstrap = False)

rf_rs.fit(train_features, train_labels)

print(rf_rs.score(train_features, train_labels))
y_pred = rf_rs.predict(test_features)
print(accuracy_score(test_labels, y_pred))

print(classification_report(test_labels, y_pred))

# %% confusion matrix & accuracy
rs_pred = cross_val_predict(rf_rs, train_features,train_labels, cv=3)
conf_matrix_rf = confusion_matrix(train_labels, rs_pred)
print(conf_matrix_rf)

plot_cm(conf_matrix_rf)

# %%
# accuracy score
print("Accuracy score: ", accuracy_score(test_labels, rs_pred))

# recall
print("Recall score: ", recall_score(test_labels, rs_pred, average=None))

# precision score
print("Precision score: ", precision_score(test_labels, rs_pred, average=None))

# %% TPOT
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt','log2']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 1000,10)]
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10,14]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4,6,8]
# Create the random grid
param = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
              'criterion':['entropy','gini']}

tpot_classifier = TPOTClassifier(generations= 5, 
                                 population_size= 24, 
                                 offspring_size= 12,
                                 verbosity= 2, 
                                 early_stop= 12,
                                 config_dict={'sklearn.ensemble.RandomForestClassifier': param}, 
                                 cv = 4, 
                                 scoring = 'accuracy')
tpot_classifier.fit(train_features, train_labels)
accuracy = tpot_classifier.score(test_features, test_labels)
print(accuracy)