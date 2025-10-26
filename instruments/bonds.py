from instrument import Instrument
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import yfinance as yf

class Bond(Instrument):
    def __init__(self, name, maturity, face_value, coupon, price=None, start_date=None,
                 frequency=None, symbol=None, timestamp=None, notes=None):
        super().__init__(self, name, timestamp, symbol, notes)
        self.start_date = datetime.today().date() if start_date is None else start_date
        self.maturity = maturity
        self.face_value = face_value
        if price is None and coupon is 0: raise ValueError('Please provide a price for zero-coupon bonds!')
        self.price = face_value if price is None else price
        self.coupon = coupon
        self.frequency = 6 if frequency is None else frequency

    def get_value(self):
        today = datetime.today().date()
        if self.maturity <= today: today = self.maturity
        dates = pd.date_range(start=self.start_date, end=today, freq='D')
        if self.coupon is 0:
            return pd.DataFrame({self.name: [self.face_value]*len(dates)}, index=pd.Index(dates, name='Date'))
        else:
            delta = relativedelta(today, self.start_date)
            n_periods = (delta.years * 12 + delta.months) // self.frequency
            interest = self.face_value * self.coupon
            value_periods = [self.face_value + i * interest for i in n_periods]
            value_series = pd.Series(index=dates, dtype=float)
            for i in n_periods:
                start = dates[0] + pd.DateOffset(months=i*self.frequency)
                end = start + pd.DateOffset(months=i*self.frequency) - pd.Timedelta(days=1)
                value_series.loc[start:end] = value_periods[i]
            value_df = pd.DataFrame({self.name: value_series})
            value_df.index.name = 'Date'
            return value_df

    def returns(self, log=False):
        if self.coupon is 0:
            returns = (self.face_value - self.price) / self.price
        else:
            returns = (self.get_value() - self.face_value) / self.face_value
        return returns if not log else np.log(1 + returns)

    def get_info(self):
        return yf.Ticker(self.symbol).info if self.symbol is not None else 'No info available.'




