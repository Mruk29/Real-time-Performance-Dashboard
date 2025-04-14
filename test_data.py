import pandas as pd

# Load dataset
file_path = r"D:\project\main copy internship.xlsx"  # Update with your correct path
df = pd.read_excel(file_path)

# Print first 5 rows
print("Columns in dataset:", df.columns)
print(df.head())
