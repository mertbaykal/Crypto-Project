import requests

def get_binance_symbols():
    url = "https://api.binance.com/api/v3/exchangeInfo"
    response = requests.get(url)
    data = response.json()
    
    symbols = []
    for item in data['symbols']:
        if item['status'] == 'TRADING' and item['quoteAsset'] == 'USDT':
            symbols.append(item['symbol'])
    return symbols

if __name__ == "__main__":
    top_symbols = get_binance_symbols()
    print(f"Top {len(top_symbols)} symbols: {top_symbols[:20]}")
