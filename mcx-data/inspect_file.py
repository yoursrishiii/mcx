import pandas as pd, glob
f = glob.glob("/Users/rishiyadav/mcx-data/files/*.xls")[0]
tables = pd.read_html(f)
df = max(tables, key=len)
df.columns = [str(c).strip() for c in df.columns]
print("COLUMNS:", list(df.columns))
print("TOTAL ROWS:", len(df))
df["Symbol"] = df["Symbol"].astype(str).str.strip()
g = df[df["Symbol"].isin(["GOLDM", "GOLDTEN", "GOLDGUINEA", "GOLDPETAL"])]
print(g.to_string())
