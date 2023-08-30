import requests
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from datetime import datetime, timedelta



def get_bitcoin_price_history():
    coin_codex_url = 'http://ec2-3-131-153-153.us-east-2.compute.amazonaws.com:3000/bitcoin/'
    response = requests.get(coin_codex_url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    
    else:
        print('Erro ao obter o histórico de preços.')
        return None

def plot_bitcoin_price(data):
    df = pd.DataFrame(data)
    df['time_period_start'] = pd.to_datetime(df['time_period_start'])
    df.set_index('time_period_start', inplace=True)
    
    # Criando o gráfico de linha
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['price_close'], marker='o', linestyle='-', color='b')
    plt.xlabel('Data')
    plt.ylabel('Preço (USD)')
    plt.title('Histórico de Preços do Bitcoin')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Obtendo o histórico de preços
bitcoin_price_data = get_bitcoin_price_history()



if bitcoin_price_data:
    # Criando o gráfico
    plot_bitcoin_price(bitcoin_price_data)




    