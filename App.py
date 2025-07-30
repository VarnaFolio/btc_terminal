from flask import Flask, render_template, request, jsonify
import ccxt
import pandas as pd
import ta

app = Flask(__name__)
exchange = ccxt.binance()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['GET'])
def analyze():
    symbol = request.args.get('pair', 'BTC/USDT')
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
    df['macd'] = ta.trend.MACD(df['close']).macd_diff()
    df['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close']).adx()

    latest = {
        'RSI': round(df['rsi'].iloc[-1], 2),
        'MACD': round(df['macd'].iloc[-1], 2),
        'ADX': round(df['adx'].iloc[-1], 2),
        'Signal': 'BUY' if df['macd'].iloc[-1] > 0 else 'SELL'
    }

    return jsonify(latest)

if __name__ == '__main__':
    app.run(debug=True)
