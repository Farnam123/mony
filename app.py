import requests
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD
from flask import Flask, render_template, request

app = Flask(__name__)

ALPHA_VANTAGE_API_KEY = "JqwuHOcwVqP55MYuz4O4K4pOscq2MWkf"

def get_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact'
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        return None

    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
    df = df.rename(columns={
        '1. open': 'open',
        '2. high': 'high',
        '3. low': 'low',
        '4. close': 'close',
        '5. volume': 'volume'
    })
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

def calculate_indicators(df):
    df['rsi'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    if latest['rsi'] < 30 and latest['macd'] > latest['macd_signal']:
        return "خرید"
    elif latest['rsi'] > 70 and latest['macd'] < latest['macd_signal']:
        return "فروش"
    else:
        return "نگهداری"

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        df = get_stock_data(symbol)
        if df is None:
            return render_template('analyze.html', error="نماد معتبر نیست یا داده‌ای یافت نشد.")
        df = calculate_indicators(df)
        signal = generate_signal(df)
        return render_template('analyze.html', signal=signal, symbol=symbol)
    return render_template('analyze.html')

if __name__ == "__main__":
    app.run(debug=True)
