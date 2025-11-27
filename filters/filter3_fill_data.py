import requests
import pandas as pd
import os
from datetime import datetime, timedelta

DATA_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/data"

BINANCE_API = "https://api.binance.com/api/v3/klines"

def download_ohlcv(symbol, start_date):
    start_ts = int(start_date.timestamp() * 1000)
    end_ts = int(datetime.now().timestamp() * 1000)

    print(f"Downloading OHLCV for {symbol} from {start_date}...")

    url = f"{BINANCE_API}?symbol={symbol}&interval=1d&startTime={start_ts}&endTime={end_ts}&limit=1000"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error:", response.text)
        return None

    data = response.json()

    rows = []
    for item in data:
        rows.append([
            datetime.utcfromtimestamp(item[0] / 1000).strftime("%Y-%m-%d"),
            float(item[1]),  # Open
            float(item[2]),  # High
            float(item[3]),  # Low
            float(item[4]),  # Close
            float(item[5])   # Volume
        ])

    df = pd.DataFrame(rows, columns=["date", "open", "high", "low", "close", "volume"])
    return df


def append_to_csv(symbol, df_new):
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")

    if os.path.exists(file_path):
        df_old = pd.read_csv(file_path)
        df = pd.concat([df_old, df_new]).drop_duplicates(subset=["date"])
    else:
        df = df_new

    df = df.sort_values("date")
    df.to_csv(file_path, index=False)
    print(f"Updated CSV saved: {file_path}")


def get_last_date(symbol):
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")

    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)

    if df.empty or "date" not in df.columns:
        return None

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    if df["date"].isnull().all():
        return None

    return df["date"].max()


if __name__ == "__main__":
    print("Filter 3 running...\n")

    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]

    for symbol in symbols:
        last_date = get_last_date(symbol)

        if last_date is None:
            start = datetime.now() - timedelta(days=3650)  # 10 years
        else:
            start = last_date + timedelta(days=1)

        df_new = download_ohlcv(symbol, start)

        if df_new is not None and not df_new.empty:
            append_to_csv(symbol, df_new)
        else:
            print(f"No new data for {symbol}.")

    print("\nFilter 3 finished.")
