#%%
from abc import ABC, abstractmethod
from datetime import datetime
import pandas as pd
import yfinance as yf

from portfolio import Portfolio

def price_history(symbol, start, end=datetime.today()):
    """Return historic asset price as a dataframe."""
    return yf.download(symbol, start=start, end=end)['Close']

class Instrument(ABC):
    """Abstract base class for financial instruments."""
    def __init__(self, name, symbol, amount=1.0, timestamp=None, notes=None):
        self.name = name
        self.symbol = symbol
        self.amount = amount
        self.timestamp = timestamp or datetime.now()
        self.notes = notes if notes is not None else ''

        active_portfolio = Portfolio.get_active()
        if active_portfolio is not None:
            active_portfolio.add_instrument(self)
        else: print(f'No active portfolio set! {self.name} not registered.')

    @classmethod
    def add_dict(cls, list_kwargs):
        """Add multiple assets of the same type at once."""
        instances = []
        for kwargs in list_kwargs:
            instances.append(cls(**kwargs))
        return instances

    @abstractmethod
    def get_value(self) -> pd.DataFrame:
        """Return historic value of asset as dataframe."""
        pass

    @abstractmethod
    def get_returns(self) -> pd.DataFrame:
        """Return historic returns of asset as dataframe."""
        pass

    @abstractmethod
    def get_info(self):
        """Return asset info as per Yahoo Finance."""
        pass

    def get_notes(self):
        """Return own notes attached to asset."""
        return f"Notes: {self.notes}\nDate added: {self.timestamp.strftime('%Y-%m-%d')}"
