import pandas as pd
import os
import numpy as np

DATA_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/data"
FEATURE_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/features"

def compute_features(symbol):
    """
    Verilen symbol için CSV'den veriyi alır ve temel feature'ları hesaplar.
    """
    file_path = os.path.join(DATA_DIR, f"{symbol}.csv")
    if not os.path.exists(file_path):
        print(f"CSV bulunamadı: {file_path}")
        return None

    df = pd.read_csv(file_path)
    if df.empty:
        print(f"CSV boş: {file_path}")
        return None

    # Tarih kolonunu datetime yap
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Log return
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))

    # Rolling volatility (7 gün)
    df['volatility_7'] = df['log_return'].rolling(window=7).std()

    # RSI (14 gün)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))

    # Moving averages
    df['MA_7'] = df['close'].rolling(window=7).mean()
    df['MA_21'] = df['close'].rolling(window=21).mean()

    # Eksik değerleri drop et
    df = df.dropna()

    # Feature CSV olarak kaydet
    os.makedirs(FEATURE_DIR, exist_ok=True)
    out_path = os.path.join(FEATURE_DIR, f"{symbol}_features.csv")
    df.to_csv(out_path, index=False)
    print(f"Features oluşturuldu: {out_path}")
    return df

if __name__ == "__main__":
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']  # Örnek
    for s in symbols:
        compute_features(s)
