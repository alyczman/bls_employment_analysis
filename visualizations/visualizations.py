import matplotlib as mpl
import pandas as pd

file_path = '../data/LaborForceParticipationRate.csv'

df = pd.read_csv(file_path)
print(df.head())

