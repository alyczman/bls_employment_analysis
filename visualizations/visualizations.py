import matplotlib as mpl
import pandas as pd

file_path = '../data/LaborForceParticipationRate.csv'

df = pd.read_csv(file_path)
print(df.head())

month_col = df['period'].str[1:]
df.insert(3, 'Month', month_col)

df['YearMonth'] = df['year'].astype('str') + df['Month']
print(df.head())