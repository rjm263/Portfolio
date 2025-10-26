from instrument import Instrument, price_history
import numpy as np
import yfinance as yf

class Stock(Instrument):
    def __init__(self, name, symbol, price, amount=1.0, timestamp=None, notes=None):
        super().__init__(name, symbol, amount, timestamp, notes)
        self.price = price

    def get_value(self):
        return price_history(self.symbol, self.timestamp) * self.amount

    def get_returns(self, log=False):
        returns = (price_history(self.symbol, self.timestamp) - self.price) / self.price
        return returns if not log else np.log(1 + returns)

    def get_info(self):
        return yf.Ticker(self.symbol).info