# Just a scratch algo for testing things out quickly

from AlgorithmImports import *
from datetime import datetime, timedelta
from decimal import Decimal

class scratch(QCAlgorithm):
    '''Basic template algorithm simply initializes the date range and cash'''

    def initialize(self) -> None:
        '''initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        self.set_time_zone(TimeZones.NEW_YORK)
        self.set_brokerage_model(BrokerageName.ALPACA)

        self._symbol = self.add_crypto("BTCUSD", Resolution.MINUTE, market=Market.COINBASE).symbol

        self.vwap = IntradayVwap(self._symbol)
        self.register_indicator(self._symbol, self.vwap, Resolution.MINUTE)
        self.warm_up_indicator(self._symbol, self.vwap, timedelta(days=1))


    def on_data(self, slice: Slice) -> None:
        '''on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.

        Arguments:
            slice: Slice object keyed by symbol containing the stock data
        '''
        if not self.vwap.is_ready:
            self.log(f'vwap value: {self.vwap.current.value}')