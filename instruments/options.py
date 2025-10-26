from instrument import Instrument, price_history
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf

# add value+return for 'write' or create new class (?)

class Option(Instrument):
    def __init__(self, name, symbol, strike, maturity, premium, amount=1.0, quantity=100, position='c', timestamp=None, notes=None):
        super().__init__(self, name, symbol, amount, timestamp, notes)
        self.strike = strike
        self.maturity = maturity
        self.premium = premium
        self.quantity = quantity
        if position is not 'c' or 'p': raise ValueError('Position argument must be \'c\' or \'p\'!')
        self.position = position

    def get_value(self):
        prices = price_history(self.symbol, self.timestamp)
        today = datetime.today().date()
        maturity_today = pd.date_range(start=self.maturity, end=today, freq='1D')
        if self.position is 'c':
            value_df = np.max(0, (prices - self.strike - self.premium) * self.amount * self.quantity)
        else:
            value_df = np.max(0, (self.strike - prices - self.premium) * self.amount * self.quantity)
        if self.maturity < today:
            value_df.loc[maturity_today] = value_df.loc[self.maturity].item()
        return value_df

    def get_returns(self, log=False):
        returns = self.get_value() / (self.premium * self.amount * self.quantity)
        return returns if not log else np.log(1 + returns)

    def get_info(self):
        return yf.Ticker(self.symbol).info



