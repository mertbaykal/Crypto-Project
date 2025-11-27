import os
import pandas as pd

DATA_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/data"

def get_last_date(symbol):
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")

    print(f"DEBUG: Checking file → {file_path}")

    if not os.path.exists(file_path):
        print("DEBUG: File not found.")
        return None

    df = pd.read_csv(file_path)
    print(f"DEBUG: CSV rows = {len(df)}")

    if df.empty:
        return None

    if "date" not in df.columns:
        print("DEBUG: 'date' column missing!")
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isnull().all():
        return None

    return df["date"].max()

if __name__ == "__main__":
    print("Filter 2 running...\n")

    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    for sym in symbols:
        last = get_last_date(sym)
        if last is None:
            print(f"{sym}: No data in CSV, full download needed.")
        else:
            print(f"{sym}: Last date = {last}")

    print("\nFilter 2 finished.")
