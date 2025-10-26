from instrument import Instrument, price_history
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf

class Future(Instrument):
    def __init__(self, name, symbol, price, margin, maturity, amount=1.0, quantity=1, position='l', timestamp=None, notes=None):
        super().__init__(self, name, symbol, amount, timestamp, notes)
        self.price = price
        self.margin = margin
        self.maturity = maturity
        self.quantity = quantity
        if position is not 'l' or 's': raise ValueError('Position must be \'l\' or \'s\'!')
        self.position = position

    def get_value(self):
        prices = price_history(self.symbol, self.timestamp)
        today = datetime.today().date()
        maturity_today = pd.date_range(start=self.maturity, end=today, freq='1D')
        value_df = (prices - self.price) * self.amount * self.quantity
        if self.maturity < today:
            value_df.loc[maturity_today] = value_df.loc[self.maturity].item()
        return value_df if self.position is 'l' else -value_df

    def get_returns(self, log=False):
        returns = self.get_value() / self.margin
        return returns if not log else np.log(1 + returns)

    def get_info(self):
        return yf.Ticker(self.symbol).info

