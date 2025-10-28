from instrument import Instrument, price_history
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf

class Future(Instrument):
    """
    Class for futures; inherits from Instrument class.

    Parameters:
    ----------
    name: str
        Name of the asset. Can be any, no need to coincide with symbol.
    symbol: str
        The symbol of the financial asset.
    price: float
        The price of the asset at time of instantiation.
    margin: float
        The margin for the futures contract. Can be adjusted by calling adjust_margin().
    maturity: str
        The maturity of the futures contract. Format: 2000-10-01
    amount: float
        The amount of identical futures contracts purchased on the underlying.
    quantity: int
        The amount of shares for one futures contract.
    position: str
        Long position ('l') or short position ('s').
    timestamp: str
        Time the asset was added to the portfolio. Format: 2000-10-01
    notes: str
        Own notes about the financial asset.
    """
    def __init__(self, name, symbol, price: float, margin: float, maturity: str, amount=1.0,
                 quantity: int=1, position: str='l', timestamp=None, notes=None):
        super().__init__(self, name, symbol, amount, timestamp, notes)
        self.price = price
        self.margin = margin
        self.maturity = datetime.strptime(maturity, '%Y-%m-%d')
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

