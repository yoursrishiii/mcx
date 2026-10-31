import os, re, glob, json, datetime as dt
import pandas as pd

FILES = os.path.expanduser("~/mcx-data/files/*.xls")
OUT = os.path.expanduser("~/mcx-data/")
# symbol: (grams in the quotation unit, purity)
C = {"GOLDM": (10, 995), "GOLDTEN": (10, 999), "GOLDGUINEA": (8, 999), "GOLDPETAL": (1, 999)}

def col(df, *keys):
    for c in df.columns:
        if all(k in c.lower() for k in keys):
            return c
    return None

rows, log, seen = [], [], set()
for f in sorted(glob.glob(FILES)):
    name = os.path.basename(f)
    m = re.search(r"_(\d{8})", name)
    req = dt.datetime.strptime(m.group(1), "%d%m%Y").date() if m else None
    try:
        df = max(pd.read_html(f), key=len)
    except Exception as e:
        log.append((name, "unreadable: " + str(e)[:50])); continue
    df.columns = [str(c).strip() for c in df.columns]
    df["Symbol"] = df["Symbol"].astype(str).str.strip()          # space-padded symbols
    df["Instrument Name"] = df["Instrument Name"].astype(str).str.strip()
    df = df[(df["Instrument Name"] == "FUTCOM") & (df["Symbol"].isin(C))].copy()  # futures only
    if df.empty:
        log.append((name, "no gold futures rows")); continue
    d = pd.to_datetime(df["Date"].astype(str).str.strip(), format="%d %b %Y", errors="coerce")
    got = d.iloc[0].date()
    if req and got != req:                                        # returned vs requested date
        log.append((name, f"date mismatch: file says {got}, name says {req}")); continue
    if got in seen:
        log.append((name, "duplicate day skipped")); continue
    seen.add(got)
    c_oi = col(df, "open", "interest")
    out = pd.DataFrame({
        "trade_date": str(got),
        "symbol": df["Symbol"].values,
        "expiry_date": pd.to_datetime(df["Expiry Date"].astype(str).str.strip().str.title(),
                                      format="%d%b%Y", errors="coerce").dt.date.astype(str).values,
        "close": pd.to_numeric(df["Close"], errors="coerce").values,
        "volume_lots": pd.to_numeric(df["Volume(Lots)"], errors="coerce").values,
        "oi": pd.to_numeric(df[c_oi], errors="coerce").values if c_oi else None,
    })
    rows.append(out)
    log.append((name, f"OK {got} {len(out)} rows"))

if not rows:
    print("Nothing usable.", log); raise SystemExit
a = pd.concat(rows)
a = a[a["close"] > 0].copy()
a["grams"] = a["symbol"].map(lambda s: C[s][0])
a["purity"] = a["symbol"].map(lambda s: C[s][1])
a["per_gram_999"] = (a["close"] / a["grams"] * 999 / a["purity"]).round(2)
a["days_to_expiry"] = (pd.to_datetime(a["expiry_date"]) - pd.to_datetime(a["trade_date"])).dt.days
a = a.sort_values(["trade_date", "symbol", "expiry_date"])
a.to_csv(OUT + "clean.csv", index=False)
with open(OUT + "data.json", "w") as fh:
    json.dump(json.loads(a.to_json(orient="records")), fh)

print("\nFILE LOG")
for n, s in log: print(" ", n, "->", s)
print(f"\nSaved clean.csv + data.json: {len(a)} rows, {a.trade_date.nunique()} trading days")
last = a[a.trade_date == a.trade_date.max()]
print("\nPER-GRAM (999) BY EXPIRY on", a.trade_date.max())
print(last.pivot_table(index="expiry_date", columns="symbol", values="per_gram_999").round(1).to_string())
