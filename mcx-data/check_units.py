import pandas as pd, glob
f = glob.glob("/Users/rishiyadav/mcx-data/files/*.xls")[0]
df = max(pd.read_html(f), key=len)
df.columns = [str(c).strip() for c in df.columns]
df["Symbol"] = df["Symbol"].astype(str).str.strip()
g = df[df["Symbol"].isin(["GOLDM", "GOLDTEN", "GOLDGUINEA", "GOLDPETAL"])].copy()
g["exp"] = pd.to_datetime(g["Expiry Date"].astype(str).str.strip(), format="%d%b%Y", errors="coerce")
g = g.sort_values(["Symbol", "exp"])
print(g[["Symbol", "Expiry Date", "Close", "Volume(Lots)"]].to_string(index=False))
