import pandas as pd
import math
import numpy as np

def readData():
    dfAll = pd.read_csv("apps/data/sample.csv")
    dfAll['lrinc'] = np.log(dfAll['rinc'] + 1)
    dfNonZero = dfAll[dfAll['lrinc'] > 0]
    return dfAll, dfNonZero

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"
