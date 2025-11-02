#!/usr/bin/env python3

import os
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime

# -----------------------
# Configuration
# -----------------------

STOCK_ETF = "VTI"   # Could also use SPY
BOND_ETF  = "BND"   # Could be any bond ETF you prefer

STOCK_PERCENT = 0.70
BOND_PERCENT  = 0.30

REBALANCE_FREQUENCY = 'W'  # 'W' for weekly, 'M' for monthly, 'D' for daily, etc.
# A real bot might run daily but only rebalance if allocations drift beyond a threshold.

# -----------------------
# Set up API
# -----------------------

api_key     = os.environ.get("APCA_API_KEY_ID")
api_secret  = os.environ.get("APCA_API_SECRET_KEY")
base_url    = os.environ.get("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")

api = tradeapi.REST(
    key_id=api_key,
    secret_key=api_secret,
    base_url=base_url
)

# -----------------------
# Utility Functions
# -----------------------

def get_account_info():
    """Fetches Alpaca account info (cash, positions, etc.)."""
    account = api.get_account()
    return account

def get_position(symbol):
    """Returns the position object for the given symbol or None if no position."""
    try:
        return api.get_position(symbol)
    except tradeapi.rest.APIError:
        return None

def place_order(symbol, qty, side, order_type="market", time_in_force="day"):
    """Places a market order with the given parameters."""
    print(f"Placing order: {side} {qty} of {symbol}")
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force
        )
    except Exception as e:
        print(f"Order failed: {e}")

def rebalance_portfolio():
    """Rebalances the portfolio to the target allocations."""

    # 1. Get current account info
    account = get_account_info()

    # Ensure we only use settled cash for a cash account scenario
    # If you're on a margin-enabled account but want to avoid margin usage,
    # you can define your logic to ensure you never buy more than your 'cash'.
    try:
        current_cash = float(account.cash)
    except:
        # fallback to buying_power if for some reason cash is not available
        current_cash = float(account.buying_power)  
        # but that might include margin, so be careful in a real environment

    # 2. Calculate total equity and target allocations
    # We want: 
    #   total_equity * 70% in STOCK_ETF
    #   total_equity * 30% in BOND_ETF
    # where total_equity is (cash + sum of positions).
    total_equity = float(account.portfolio_value)

    target_stock_dollars = total_equity * STOCK_PERCENT
    target_bond_dollars  = total_equity * BOND_PERCENT

    # 3. Get current positions
    stock_pos = get_position(STOCK_ETF)
    bond_pos  = get_position(BOND_ETF)

    # Current position amounts in dollars
    current_stock_value = float(stock_pos.market_value) if stock_pos else 0.0
    current_bond_value  = float(bond_pos.market_value)  if bond_pos  else 0.0

    # 4. Check if we need to sell or buy STOCK_ETF
    #    We'll do it in a naive manner: sell if above target, buy if below target.
    if current_stock_value > target_stock_dollars:
        # Sell the difference (in shares)
        difference = current_stock_value - target_stock_dollars
        # We need the price to convert difference in dollars to shares
        last_trade = api.get_latest_trade(STOCK_ETF)
        current_price = float(last_trade.price)
        shares_to_sell = int(difference // current_price)
        if shares_to_sell > 0:
            place_order(STOCK_ETF, shares_to_sell, "sell")
    else:
        # Buy the difference
        difference = target_stock_dollars - current_stock_value
        last_trade = api.get_latest_trade(STOCK_ETF)
        current_price = float(last_trade.price)
        shares_to_buy = int(difference // current_price)
        # Ensure we have enough cash
        if shares_to_buy > 0 and shares_to_buy * current_price <= current_cash:
            place_order(STOCK_ETF, shares_to_buy, "buy")
            current_cash -= (shares_to_buy * current_price)

    # 5. Check if we need to sell or buy BOND_ETF
    if current_bond_value > target_bond_dollars:
        # Sell
        difference = current_bond_value - target_bond_dollars
        last_trade = api.get_latest_trade(BOND_ETF)
        current_price = float(last_trade.price)
        shares_to_sell = int(difference // current_price)
        if shares_to_sell > 0:
            place_order(BOND_ETF, shares_to_sell, "sell")
    else:
        # Buy
        difference = target_bond_dollars - current_bond_value
        last_trade = api.get_latest_trade(BOND_ETF)
        current_price = float(last_trade.price)
        shares_to_buy = int(difference // current_price)
        # Ensure we have enough cash
        if shares_to_buy > 0 and shares_to_buy * current_price <= current_cash:
            place_order(BOND_ETF, shares_to_buy, "buy")
            current_cash -= (shares_to_buy * current_price)

def should_rebalance():
    """Decides if it is time to rebalance (weekly, monthly, etc.). 
       For simplicity, let's do a naive check by day-of-month or day-of-week."""
    now = datetime.now()
    
    if REBALANCE_FREQUENCY == 'D':
        return True
    elif REBALANCE_FREQUENCY == 'W':
        # Rebalance every Monday, for example
        return now.weekday() == 0  # Monday=0, Tuesday=1, ...
    elif REBALANCE_FREQUENCY == 'M':
        # Rebalance on the 1st of each month
        return now.day == 1
    else:
        # Default: no rebalancing
        return False

def main():
    if should_rebalance():
        print(f"Rebalancing on {datetime.now()}")
        rebalance_portfolio()
    else:
        print(f"No rebalance today ({datetime.now()})")

if __name__ == "__main__":
    main()