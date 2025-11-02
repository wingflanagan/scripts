import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np

class MeanReversionBot:
    def __init__(self):
        self.api = tradeapi.REST()
        self.symbols = ['SPY', 'IWM', 'TLT']  # Diversified ETFs
        self.bb_window = 20
        
    def calculate_bands(self, data):
        sma = data.close.rolling(self.bb_window).mean()
        std = data.close.rolling(self.bb_window).std()
        return sma, sma + 2*std, sma - 2*std
        
    def run_strategy(self):
        for symbol in self.symbols:
            # Get data
            bars = self.api.get_bars(symbol, 'day', limit=self.bb_window+1).df
            
            # Calculate indicators
            upper_band, _, lower_band = self.calculate_bands(bars)
            current_price = bars.close[-1]
            
            # Get position and cash
            position = self.api.get_position(symbol) if self.api.get_asset(symbol).tradable else None
            cash = float(self.api.get_account().cash)
            
            # Trading logic
            if current_price < lower_band[-1] and cash > 100:
                # Buy signal
                qty = min(int((cash * 0.01) // current_price), 1)  # 1% position
                self.api.submit_order(symbol, qty=qty, side='buy', type='market')
                
            elif current_price > upper_band[-1] and position:
                # Sell signal
                self.api.submit_order(symbol, qty=position.qty, side='sell', type='market')

if __name__ == "__main__":
    bot = MeanReversionBot()
    bot.run_strategy()