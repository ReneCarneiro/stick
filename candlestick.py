import requests
from pymongo import MongoClient
import pandas as pd

from datetime import datetime


import mplfinance as mpf

mongo_url = 'mongodb+srv://vitordev:bitcoin123@cluster0.muupqh8.mongodb.net/'
db_name = 'bitcoin'
collection_name = 'bitcoin-price-history'

headers = {
    'X-CoinAPI-Key': 'B71970C4-71D8-4F1D-B5B2-2B5CE1A7F273'
}

client = MongoClient(mongo_url)
db = client[db_name]
collection = db[collection_name]

def convert_to_timestamp(date_str):
    dt_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f000000Z")
    timestamp = dt_obj.timestamp()
    return timestamp


def get_bitcoin_price_history():
    coin_codex_url = 'https://rest.coinapi.io/v1/ohlcv/BITSTAMP_SPOT_BTC_USD/history?period_id=1DAY&time_start=2023-07-25T00:00:00Z&time_end=2023-08-25T00:00:00Z'
    response = requests.get(coin_codex_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        for entry in data:
            entry["time_period_start"] = convert_to_timestamp(entry["time_period_start"])
            entry["time_period_end"] = convert_to_timestamp(entry["time_period_end"])
        # collection.insert_one(data)
        return data
    else:
        print('Erro ao obter o histórico de preços.')
        return None

def plot_bitcoin_price_candlestick(data): 
    df = pd.DataFrame(data, columns=['time_period_start', 'time_period_end', 'time_open', 'time_close', 'price_open','price_high','price_low','price_close','volume_traded','trades_count'])
    df.index = pd.to_datetime(df['time_period_start'], unit='s')
    
    candlestick_df = pd.DataFrame()
    candlestick_df['Open'] = df['price_open']
    candlestick_df['High'] = df['price_high']
    candlestick_df['Low'] = df['price_low']
    candlestick_df['Close'] = df['price_close']
    candlestick_df['Date'] = pd.to_datetime(df['time_period_start'])
    
    style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 8})
    mpf.plot(candlestick_df, type='candle', style=style, title="Preço do Bitcoin no mês de Agosto", ylabel="Preço(U$)",xlabel="Data")


bitcoin_price_data = get_bitcoin_price_history()


if bitcoin_price_data:
    plot_bitcoin_price_candlestick(bitcoin_price_data)




    