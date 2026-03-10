import pandas as pd
import sqlite3

# Load CSV
df = pd.read_csv("data/sales.csv")

# Connect to SQLite database
conn = sqlite3.connect("data/sales.db")

# Write table
df.to_sql("sales", conn, if_exists="replace", index=False)

print("Database created successfully!")

conn.close()