# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 14:37:57 2016

@author: odz197
"""

import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from operator import is_not
from functools import partial
import math
import re

#load our cutomized data load module
import loaddata

#this code read files under two folder and merge them together into one data frame
#1 Read mojo files
mojo_data = loaddata.load_mojo_data()
mojo_df = pd.DataFrame(mojo_data)
mojo_df['title_clean'] = mojo_df['title'].str.replace('[^\w]','').str.lower()
#2 Read meta files
meta_data = loaddata.load_metacritic_data()
meta_df = pd.DataFrame(meta_data)
meta_df['title_clean'] = meta_df['title'].str.replace('[^\w]','').str.lower()
#3 Merge two file together
df_merged = pd.merge(mojo_df, 
                     meta_df,
                     on='title_clean',
                     how = 'left')
# check the final data frame
list(df_merged.columns.values)
df_merged

# Feature engineering
df_merged['international_gross'] = df_merged.worldwide_gross - df_merged.domestic_gross
df_merged['domestic_margin'] = (df_merged.domestic_gross - df_merged.production_budget) / df_merged.production_budget
df_merged['worldwide_margin'] = (df_merged.worldwide_gross - df_merged.production_budget) / df_merged.production_budget
df_merged.describe()

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=40)
num_features = ['worldwide_gross',
                'opening_per_theater',
                'opening_weekend_take',
                'production_budget',
                'widest_release',
                'metascore',
#                'num_critic_reviews',
                'num_user_ratings',
#                'num_user_reviews',
                'runtime_minutes']
                         
data = df_merged[num_features].dropna()
X = data.iloc[:,1:].values
Y = data.iloc[:,1].values
forest.fit(X,Y)






