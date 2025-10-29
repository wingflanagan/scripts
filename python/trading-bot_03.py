import os
import csv
import datetime
import time
from alpaca_trade_api import REST, TimeFrame
import numpy as np
import yaml

##########################################
# Configuration
##########################################
# Example config.yaml:
# alpaca:
#   api_key: "YOUR_ALPACA_API_KEY"
#   secret_key: "YOUR_ALPACA_SECRET_KEY"
#   base_url: "https://paper-api.alpaca.markets"
# trading:
#   risk_factor: 1.0
#   initial_symbols: ["AAPL", "MSFT", "SPY"]
#   short_term_window: 20
#   long_term_window: 50

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

ALPACA_API_KEY = config['alpaca']['api_key']
ALPACA_SECRET_KEY = config['alpaca']['secret_key']
ALPACA_BASE_URL = config['alpaca']['base_url']

risk_factor = config['trading']['risk_factor']  # e.g. 0.5 (lower), 1.0 (medium), 2.0 (high)
symbols = config['trading']['initial_symbols']
short_term_window = config['trading']['short_term_window']
long_term_window = config['trading']['long_term_window']

alpaca = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL)

##########################################
# Helper Functions
##########################################

def get_account_info():
    return alpaca.get_account()

def get_buying_power():
    # We’ll interpret buying_power as cash since we don't want to use margin.
    # Alpaca’s paper trading gives "buying_power" but also "cash".
    account = get_account_info()
    return float(account.cash)

def get_positions():
    return alpaca.list_positions()

def get_historical_data(symbol, start_date, end_date):
    # fetch daily bars
    bars = alpaca.get_bars(symbol, TimeFrame.Day, start_date, end_date, adjustment='raw')
    # Return closing prices only
    closes = [bar.c for bar in bars]
    return closes

def compute_moving_average(prices, window):
    if len(prices) < window:
        return None
    return np.mean(prices[-window:])

def place_order(symbol, qty, side='buy'):
    order = alpaca.submit_order(
        symbol=symbol,
        qty=qty,
        side=side,
        type='market',
        time_in_force='day'
    )
    return order

def log_trades(orders):
    today_str = datetime.date.today().isoformat()
    filename = f"trades_{today_str}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Symbol", "Action", "Quantity", "Datetime"])
        for o in orders:
            writer.writerow(o)

##########################################
# Strategy & Execution
##########################################

def get_portfolio_dict():
    positions = get_positions()
    portfolio = {p.symbol: float(p.qty) for p in positions}
    return portfolio

def run_strategy():
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=365)).isoformat()
    end_date = today.isoformat()

    # Simple trend-following strategy:
    # If short-term MA > long-term MA: ensure we're long.
    # If short-term MA < long-term MA: ensure we're flat (no position).

    portfolio = get_portfolio_dict()
    cash = get_buying_power()
    orders = []

    # Determine how much cash to allocate per symbol
    # A simple heuristic: use some fraction of cash per symbol based on risk_factor
    # For example, allocate (risk_factor * 10%) of cash per symbol if conditions are met.
    allocation_per_symbol = cash * 0.10 * risk_factor

    for sym in symbols:
        prices = get_historical_data(sym, start_date, end_date)
        if len(prices) < long_term_window:
            continue

        short_ma = compute_moving_average(prices, short_term_window)
        long_ma = compute_moving_average(prices, long_term_window)
        current_price = prices[-1]

        held_qty = portfolio.get(sym, 0.0)

        if short_ma is not None and long_ma is not None:
            if short_ma > long_ma:
                # Trend up: want to be long
                if held_qty == 0 and allocation_per_symbol > current_price:
                    # Buy as many shares as allocation_per_symbol allows
                    qty_to_buy = int(allocation_per_symbol // current_price)
                    if qty_to_buy > 0 and qty_to_buy * current_price <= cash:
                        order = place_order(sym, qty_to_buy, side='buy')
                        orders.append([sym, 'BUY', qty_to_buy, datetime.datetime.now()])
            else:
                # Trend down: want to be flat
                if held_qty > 0:
                    order = place_order(sym, held_qty, side='sell')
                    orders.append([sym, 'SELL', held_qty, datetime.datetime.now()])

    # Log the orders
    if orders:
        log_trades(orders)

##########################################
# Main Loop
##########################################

def main():
    # In real use, you'd run this once a day, maybe with a cron job.
    # For demonstration, just run once here.
    run_strategy()

if __name__ == "__main__":
    main()
