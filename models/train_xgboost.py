import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import xgboost as xgb

FEATURE_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/features"
MODEL_DIR = "/Users/mertbaykal/Desktop/CryptoProject1/models"

def load_features(symbol):
    file_path = os.path.join(FEATURE_DIR, f"{symbol}_features.csv")
    if not os.path.exists(file_path):
        print(f"[ERROR] Features bulunamadı: {file_path}")
        return None

    df = pd.read_csv(file_path)
    df = df.sort_values("date")
    df['label'] = (df['close'].shift(-1) > df['close']).astype(int)
    df = df.dropna()
    print(f"[INFO] {symbol} data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

if __name__ == "__main__":
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    df_list = []

    for s in symbols:
        df = load_features(s)
        if df is not None:
            df_list.append(df)

    if not df_list:
        print("[ERROR] Hiç veri yüklenemedi. Çıkılıyor.")
        exit()

    data = pd.concat(df_list)
    features = ['log_return', 'volatility_7', 'RSI_14', 'MA_7', 'MA_21']
    X = data[features]
    y = data['label']

    print(f"[INFO] Combined data shape: {data.shape}")
    print(f"[INFO] Feature matrix X shape: {X.shape}")
    print(f"[INFO] Target vector y shape: {y.shape}")
    print(f"[INFO] Sample X head:\n{X.head()}")
    print(f"[INFO] Sample y head:\n{y.head()}")

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    print(f"[INFO] Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")

    # XGBoost modeli
    model = xgb.XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )

    print("[INFO] Model eğitiliyor...")
    model.fit(X_train, y_train)

    # Tahmin ve skor
    y_pred = model.predict(X_test)
    print("[INFO] Model değerlendirme:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))
    print("ROC AUC:", roc_auc_score(y_test, y_pred))

    # Model kaydet
    os.makedirs(MODEL_DIR, exist_ok=True)
    model_path = os.path.join(MODEL_DIR, "xgb_model.json")
    model.save_model(model_path)
    print(f"[INFO] Model kaydedildi: {model_path}")
