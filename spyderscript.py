import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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
                     on=['title_clean','year'],
                     how = 'left')
# check the final data frame
df_merged.head()



df_merged['international_gross'] = df_merged.worldwide_gross - df_merged.domestic_gross
df_merged['domestic_margin'] = (df_merged.domestic_gross - df_merged.production_budget) / df_merged.production_budget
df_merged['worldwide_margin'] = (df_merged.worldwide_gross - df_merged.production_budget) / df_merged.production_budget
df_recent = df_merged[df_merged['year']>=1988]
df_recent.describe()