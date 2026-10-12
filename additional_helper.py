import pandas as pd

df = pd.read_json("Selected_procedures.json")
print(df.columns.tolist())
print(df["Under 25 (Number)"].dtype)
print(df["Under 25 (Number)"].head())


