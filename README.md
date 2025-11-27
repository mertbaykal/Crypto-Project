# Crypto Project – Homework 1

## Project Overview

This project focuses on analyzing historical cryptocurrency data from international exchanges using a **Pipe and Filter architecture**. The application automates the download, transformation, and storage of data for the top 1000 active cryptocurrencies. The processed data spans the last 10 years on a daily basis and includes relevant financial information such as OHLCV (Open, High, Low, Close, Volume), volatility, and other key indicators.

The main goal is to provide a clean and structured dataset for further analysis and modeling, such as predicting price movements using machine learning algorithms.

## Technologies Used

* Python 3.9
* Pandas, NumPy for data processing
* Requests for API calls
* XGBoost for model training
* CSV files for storing processed data

## Data Sources

* Binance API (primary data source)
* Only active, valid cryptocurrency symbols were considered. Delisted, low-liquidity, or unstable pairs were excluded automatically.

## Project Structure

```
CryptoProject/
│
├── filters/
│   ├── filter1_symbols.py       # Downloads and filters top 1000 symbols
│   ├── filter2_check_dates.py   # Checks last available date for each symbol
│   └── filter3_fill_data.py     # Fills missing data and updates CSVs
│
├── data/                        # Stores raw and updated cryptocurrency data (CSV)
│
├── features/                    # Stores generated features for model training
│   └── feature_generator.py     # Generates indicators and technical features
│
├── models/
│   └── train_xgboost.py         # Trains an XGBoost model using generated features
│
├── main.py                       # Runs the entire pipeline sequentially
└── requirements.txt             # Required Python packages
```

## Pipeline Description

The project implements a **Pipe and Filter** architecture:

1. **Filter 1 – Symbols**: Automatically retrieves the top 1000 active cryptocurrency symbols from Binance and filters out invalid or duplicate entries.
2. **Filter 2 – Check Dates**: Checks each CSV file to identify the last recorded date for each cryptocurrency.
3. **Filter 3 – Fill Data**: Downloads missing historical data up to the current date and updates the CSVs.
4. **Feature Generation**: Creates technical features (e.g., log returns, moving averages, RSI, volatility) from the data for model input.
5. **Model Training**: Trains an XGBoost model to predict short-term price movements using the generated features.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/mertbaykal/Crypto-Project.git
cd Crypto-Project
```

2. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the pipeline:

```bash
python3 main.py
```

This will execute all filters, generate features, and train the model sequentially.

## Results

* All data is stored in the `data/` folder.
* Generated features are stored in the `features/` folder.
* The trained XGBoost model is saved in `models/xgb_model.json`.


