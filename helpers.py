import os
import pandas as pd
import numpy as np

def readData():
    """Read CSV data once. DATA_DIR env var can override default folder."""
    data_dir = os.getenv("DATA_DIR", "apps/data")
    path = os.path.join(data_dir, "sample.csv")
    dfAll = pd.read_csv(path)
    dfAll['lrinc'] = np.log(dfAll['rinc'] + 1)
    dfNonZero = dfAll[dfAll['lrinc'] > 0]
    return dfAll, dfNonZero

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"
