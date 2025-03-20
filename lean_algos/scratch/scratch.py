# Just a scratch algo for testing things out quickly

from AlgorithmImports import *
from datetime import datetime, timedelta
from decimal import Decimal

class scratch(QCAlgorithm):
    '''Basic template algorithm simply initializes the date range and cash'''

    def initialize(self) -> None:
        '''initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        self.set_time_zone(TimeZones.NEW_YORK)
        self.set_brokerage_model(BrokerageName.ALPACA, AccountType.MARGIN)

        self._symbol = self.add_equity('AAPL', resolution=Resolution.Minute, extended_market_hours=False).symbol 

        
        security = self.securities['AAPL']
        security.set_leverage(2)

        # Get available buying power for the security
        available_buying_power = self.portfolio.get_buying_power(self._symbol, OrderDirection.SELL)
        LEVERAGE_MULTIPLIER = 2
        cash = self.portfolio.cash
        leveraged_cash = self.portfolio.cash * LEVERAGE_MULTIPLIER

        # Position      Side	                Condition	                    Margin Requirement
        # LONG	        share price < $2.50	    100% of EOD market value
        # LONG	        share price >= $2.50	30% of EOD market value
        # LONG	        2x Leveraged ETF	    100% of EOD market value
        # LONG	        3x Leveraged ETF	    100% of EOD market value
        # SHORT	        share price < $5.00	    Greater of $2.50/share or 100%
        # SHORT	        share price >= $5.00	Greater of $5.00/share or 30%
        
        buying_power_model = security.buying_power_model
        self.log(f'buying power model: {buying_power_model}')

        parameter = InitialMarginParameters(security, 1.0)
        initial_margin_value = security.buying_power_model.get_initial_margin_requirement(parameter).value

        # parameter = MaintenanceMarginParameters(security, 1.0)
        # maintenance_margin = security.buying_power_model.get_maintenance_margin_requirement(parameter)

        self.log(f"available_buying_power: {available_buying_power}")
        self.log(f"cash: {cash}")
        self.log(f"leveraged_cash: {leveraged_cash}")
        self.log(f"initial_margin: {initial_margin_value}")
        # self.log(f"maintenance_margin: {maintenance_margin}")
        # self.log(f"{self.portfolio.log_margin_information()}")

    def on_data(self, slice: Slice) -> None:
        '''on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.

        Arguments:
            slice: Slice object keyed by symbol containing the stock data
        '''
        pass