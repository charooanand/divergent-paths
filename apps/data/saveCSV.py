import pandas as pd
import numpy as np

dfTab = pd.read_stata("replicationData/Data/data_tab.dta", convert_categoricals = False)
dfSample = dfTab.sample(frac=0.01, random_state=42)
dfSample.to_csv("apps/data/sample.csv", index=False)

# def duplicate_by_weight(df, weight_col):
#     # Ensure weight column contains integers
#     df[weight_col] = df[weight_col].astype(int)
#
#     # Create an index repeating each row index by its weight
#     repeated_index = np.repeat(df.index, df[weight_col])
#
#     # Create the new dataframe using the repeated index
#     expanded_df = df.loc[repeated_index].reset_index(drop=True)
#
#     return expanded_df
#
# dfTabWeighted = duplicate_by_weight(dfTab, 'perwt')
