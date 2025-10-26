import pandas as pd
from stocks import Stock
from savings_plans import SavingsPlan
from bonds import Bond
from futures import Future
from options import Option

class Portfolio:
    """Container class for all assets; grouped by type."""
    active_portfolio = None

    def __init__(self):
        self.stocks = []
        self.savings_plans = []
        self.bonds = []
        self.futures = []
        self.options = []
        self.cash = pd.DataFrame({'Origin': [], 'Amount': []})
        self.cash.index.name = 'Date'

    @classmethod
    def set_active(cls, portfolio):
        """Set portfolio into which instruments are registered."""
        cls.active_portfolio = portfolio

    @classmethod
    def get_active(cls):
        """Return active portfolio."""
        return cls.active_portfolio

    def add_instrument(self, instrument):
        """Add instruments to respective list."""
        if isinstance(instrument, Stock):
            self.stocks[instrument.name] = instrument
        elif isinstance(instrument, SavingsPlan):
            self.savings_plans[instrument.name] = instrument
        elif isinstance(instrument, Bond):
            self.bonds[instrument.name] = instrument
        elif isinstance(instrument, Future):
            self.futures[instrument.name] = instrument
        elif isinstance(instrument, Option):
            self.options[instrument.name] = instrument
        else: raise ValueError('Instrument type not included in portfolio!')

    def add_cash(self, origin, amount):
        """Add amount of cash from origin to cash account."""
        today = pd.to_datetime("today")
        self.cash.loc[today] = [origin, amount]

    def get_total_value(self):
        """Return total value per asset class and of portfolio."""
        total_stocks = sum([s.get_value().iloc(-1).item() for s in self.stocks])
        total_savings_plans = sum([s.get_value().iloc(-1).item() for s in self.savings_plans])
        total_bonds = sum([s.get_value().iloc(-1).item() for s in self.bonds])
        total_futures = sum([s.get_value().iloc(-1).item() for s in self.futures])
        total_options = sum([s.get_value().iloc(-1).item() for s in self.options])
        total_value = (total_stocks + total_savings_plans + total_bonds + total_futures +
                       total_options + self.cash['amount'].sum())
        print(f'Value stocks: {total_stocks}\nValue savings plans: {total_savings_plans}\nValue bonds: '
              f'{total_bonds}\nValue futures: {total_futures}\nValue options: '
              f'{total_options}\n\nTotal value: {total_value}')

