import pandas as pd
from crawler import *

df = pd.read_pickle("user_data")
clicking(df.loc["test", :])


