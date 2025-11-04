import pandas as pd
import requests
import json
from sqlalchemy import create_engine
import time
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("aiven_string"))

symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "DOTUSDT", "TRXUSDT",
    "MATICUSDT", "LTCUSDT", "LINKUSDT", "BCHUSDT", "XLMUSDT",
    "ATOMUSDT", "UNIUSDT", "ETCUSDT", "NEARUSDT", "APTUSDT"
]

def extract_binance_data():
    api_url = os.getenv("24hr_data")                
    response = requests.get(api_url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "symbol", "priceChange", "priceChangePercent", "lastPrice",
        "bidPrice", "openPrice", "highPrice", "lowPrice", "volume",
        "openTime", "closeTime"
    ])
    df = df[df['symbol'].isin(symbols)]
    
    
    numeric_cols = ["priceChange", "priceChangePercent", "lastPrice", "bidPrice", 
                   "openPrice", "highPrice", "lowPrice", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
    
def extract_binance_prices():
    api_url = os.getenv("prices")
    response = requests.get(api_url)
    data = response.json()
    df = pd.DataFrame(data, columns=["symbol", "price"])
    df = df[df['symbol'].isin(symbols)]
    
   
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    
    return df

def recent_trades():
    main_data = []
    for symbol in symbols:
        api_url = os.getenv("trades")
        response = requests.get(api_url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "id", "price", "qty", "quoteQty", "time", "isBuyerMaker", "isBestMatch"
        ])
        df['symbol'] = symbol
        
        
        numeric_cols = ["price", "qty", "quoteQty"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        main_data.append(df)
    final_df = pd.concat(main_data, ignore_index=True)
    return final_df

def klines():
    main_data = []
    interval = "30m"
    for symbol in symbols:
        api_url = os.getenv("klines")
        response = requests.get(api_url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "openTime", "open", "high", "low", "close", "volume",
            "closeTime", "quoteAssetVolume", "numberOfTrades",
            "takerBuyBaseAssetVolume", "takerBuyQuoteAssetVolume", "ignore"
        ])
        
        df['symbol'] = symbol
        
      
        numeric_cols = ["open", "high", "low", "close", "volume", "quoteAssetVolume", 
                       "takerBuyBaseAssetVolume", "takerBuyQuoteAssetVolume", "ignore"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
        main_data.append(df)
    final_df = pd.concat(main_data, ignore_index=True)
    return final_df

def to_sql(df, table_name):
    df.to_sql(table_name, engine, schema='binance_schema', if_exists="replace", index=False)


while True:
 
    binance_data = extract_binance_data()
    binance_prices = extract_binance_prices() 
    recent_trades_data = recent_trades()
    candlesticks_data = klines()
    
    
    to_sql(binance_data, "binance_24hrdata")
    to_sql(binance_prices, "binance_prices")
    to_sql(recent_trades_data, "binance_recent_trades")
    to_sql(candlesticks_data, "binance_candlesticks")
    
    print("Data extracted and loaded successfully. Waiting 2 mins for next run.......")
    time.sleep(120)