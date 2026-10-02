import argparse, json, time, datetime as dt
import requests, pandas as pd

URL = "https://www.mcxindia.com/backpage.aspx/GetDateWiseBhavCopy"
HEAD = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.mcxindia.com/market-data/bhavcopy",
}
# symbol: (grams in the QUOTATION unit, purity). VERIFY on MCX contract specs.
CONTRACTS = {
    "GOLDM": (10, 995),
    "GOLDTEN": (10, 999),
    "GOLDGUINEA": (8, 999),
    "GOLDPETAL": (1, 999),
}

def fetch(day):
    r = requests.post(URL, headers=HEAD, timeout=30,
                      json={"Date": day.strftime("%Y%m%d"), "InstrumentName": "ALL"})
    r.raise_for_status()
    return r.json().get("d", {}).get("Data", []) or []

def pick(cols, *keys):
    for c in cols:
        if all(k in c for k in keys):
            return c
    return None

def main(days):
    out, skipped = [], []
    today = dt.date.today()
    for i in range(days):
        day = today - dt.timedelta(days=i)
        if day.weekday() >= 5:
            continue
        try:
            rows = fetch(day)
        except Exception as e:
            skipped.append((str(day), str(e)[:60])); continue
        if not rows:
            skipped.append((str(day), "no data (holiday?)")); continue
        df = pd.DataFrame(rows)
        df.columns = [c.lower().replace(" ", "") for c in df.columns]
        c_sym = pick(df.columns, "symbol")
        c_exp = pick(df.columns, "expiry")
        c_close = pick(df.columns, "close")
        c_vol = pick(df.columns, "volume", "lots") or pick(df.columns, "volume")
        c_oi = pick(df.columns, "openinterest")
        c_date = pick(df.columns, "date")
        df["symbol"] = df[c_sym].astype(str).str.strip()
        df = df[df["symbol"].isin(CONTRACTS)].copy()
        if df.empty:
            continue
        ok = False
        if c_date:
            raw = str(df[c_date].iloc[0])
            for dayfirst in (False, True):
                try:
                    if pd.to_datetime(raw, dayfirst=dayfirst).date() == day:
                        ok = True; break
                except Exception:
                    pass
        if c_date and not ok:
            skipped.append((str(day), "returned date != requested date")); continue
        df["trade_date"] = str(day)
        df["expiry_date"] = pd.to_datetime(df[c_exp].astype(str).str.strip(),
                                           format="%d%b%Y", errors="coerce") \
                              .fillna(pd.to_datetime(df[c_exp], errors="coerce")).dt.date.astype(str)
        df["close"] = pd.to_numeric(df[c_close], errors="coerce")
        df["volume"] = pd.to_numeric(df[c_vol], errors="coerce") if c_vol else None
        df["oi"] = pd.to_numeric(df[c_oi], errors="coerce") if c_oi else None
        df["grams"] = df["symbol"].map(lambda s: CONTRACTS[s][0])
        df["purity"] = df["symbol"].map(lambda s: CONTRACTS[s][1])
        df["per_gram_999"] = df["close"] / df["grams"] * (999 / df["purity"])
        out.append(df[["trade_date", "symbol", "expiry_date", "close", "volume", "oi",
                       "grams", "purity", "per_gram_999"]])
        print("OK", day, len(df), "rows")
        time.sleep(1)
    if not out:
        print("No data fetched. Skipped:", skipped); return
    clean = pd.concat(out).sort_values(["trade_date", "symbol", "expiry_date"])
    clean.to_csv("clean.csv", index=False)
    with open("data.json", "w") as f:
        json.dump(json.loads(clean.to_json(orient="records")), f)
    print(f"\nSaved clean.csv and data.json: {len(clean)} rows, "
          f"{clean.trade_date.nunique()} trading days, {len(skipped)} skipped")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    main(ap.parse_args().days)
