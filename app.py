from flask import Flask, jsonify, render_template
import yfinance as yf
import threading
import time
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

#app = Flask(__name__)
app = Flask("__name__")

# List of stock tickers to monitor
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "NVDA"]

# Dictionary to store the latest market data and investment performance
market_data = {ticker: {} for ticker in tickers}

def fetch_market_data():
    global market_data
    while True:
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1y")
            if not data.empty:
                # Latest data
                latest_price = data['Close'].iloc[-1]
                # Price from one year ago
                one_year_ago_price = data['Close'].iloc[0]
                # Calculate performance
                initial_investment = 1000
                current_value = (latest_price / one_year_ago_price) * initial_investment
                performance = current_value - initial_investment

                market_data[ticker] = {
                    "latest_price": latest_price,
                    "one_year_ago_price": one_year_ago_price,
                    "initial_investment": initial_investment,
                    "current_value": current_value,
                    "performance": performance
                }
        time.sleep(60)  # Fetch new data every 60 seconds

@app.route('/')
def index():
    return render_template('index.html', market_data=market_data)

@app.route('/api/market_data')
def get_market_data():
    return jsonify(market_data)

if __name__ == '__main__':
    # Start the background thread to fetch market data
    data_thread = threading.Thread(target=fetch_market_data)
    data_thread.start()

    app.run(debug=True)