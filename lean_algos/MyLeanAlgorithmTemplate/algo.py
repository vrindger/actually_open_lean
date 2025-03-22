from AlgorithmImports import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "redacted"
SENDER_PASSWORD = "redacted"
RECIPIENT_EMAIL = "redacted"

# GLOBAL HARDCODES


INDEX_TICKER_LIST = ['SPY', 'QQQ', 'DIA']

TARGET_ACCOUNT_ALLOCATION_PER_TRADE = 0.01
MAX_ACCOUNT_ALLOCATION_PCT = 0.70
LONG_TRAILING_STOP_PCT = 4 # 2%
SHORT_TRAILING_STOP_PCT = 4 # 2%

LEVERAGE_MULTIPLIER = 2

def send_email_notification(subject, body, sender_email, sender_password, recipient_email):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)  # Log in to the server

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        server.quit()  # Close the connection to the server

def email(subject, body=''):
    send_email_notification(subject, body, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL)


def email_and_log(message, algorithm=None, body=''):
    if body:
        email(subject=message, body=body)
    else:
        email(subject=message, body='')

    if algorithm:
        algorithm.log(f'{message}\n{body}')

class MyLeanAlgorithm(QCAlgorithm):
    '''Basic template algorithm simply initializes the date range and cash'''

    def initialize(self) -> None:
        '''initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        self.set_time_zone(TimeZones.NEW_YORK)
        self.target_trade_allocation_pct = 0.01  # 1% per trade, adjust as needed
        self.max_account_allocation_pct = 0.70  # 70% of portfolio to be used
        self.account_allocation_per_trade = 0.0

        self.spy_symbol = self.add_equity('SPY', resolution=Resolution.Minute, extended_market_hours=False).symbol

    def on_data(self, slice: Slice) -> None:
        '''on_data event is the primary entry point for your algorithm. Each new data point will be pumped in here.

        Arguments:
            slice: Slice object keyed by symbol containing the stock data
        '''
        if not self.portfolio[self.spy_symbol].invested:
            self.ensure_long_position(self.spy_symbol, slice.bars[self.spy_symbol].close)

     
        """
        Calculates the percentage of the portfolio to allocate per trade,
        ensuring it doesn't exceed the maximum portfolio allocation.

        Args:
            num_stocks_to_trade: The number of stocks to trade for the day.
        """
        if num_stocks_to_trade <= 0:
            self.log("initialize_allocation: No stocks to trade")
            self.account_allocation_per_trade = 0.0
            return

        # calculate ideal allocation by distributing max_account_allocation_pct evenly
        ideal_allocation_per_trade = self.max_account_allocation_pct / num_stocks_to_trade

        # choose the smaller of ideal allocation and target allocation.
        self.account_allocation_per_trade = min(ideal_allocation_per_trade, self.target_trade_allocation_pct)

        self.log(
            f"initialize_allocation: Number of Stocks: {num_stocks_to_trade}, Ideal Allocation: {ideal_allocation_per_trade:.4f}, Target Allocation: {self.target_trade_allocation_pct:.4f}, Final Allocation: {self.account_allocation_per_trade:.4f}"
        )

    def calculate_order_quantity(self, symbol, price, order_direction):
        """
        Calculates the order quantity for a given symbol, considering available buying power,
        margin requirements, and the configured allocation percentage.
        Prefers buying at least 1 stock.

        Args:
            symbol: The symbol object of the stock.
            price: The current price of the stock.

        Returns:
            The order quantity (positive for long, negative for short), or 0 if no trade should be made.
        """
        if self.account_allocation_per_trade <= 0:
            self.log(
                f"calculate_order_quantity: {symbol}: account_allocation_per_trade is 0 or less. Cannot calculate quantity."
            )
            return 0

        if price <= 0:
            self.log(
                f"calculate_order_quantity: {symbol}: Price is 0 or less, cannot calculate quantity."
            )
            return 0
        
        security = self.securities[symbol]
        buying_power_model = security.buying_power_model

        # Get available buying power for the security
        params = BuyingPowerParameters(self.portfolio, security, order_direction)
        available_buying_power = buying_power_model.get_buying_power(params).value
        # initial_margin_requirement = buying_power_model.get_initial_margin_requirement(security, self.portfolio)
        # maintenance_margin_requirement = buying_power_model.get_maintenance_margin(security, self.portfolio)

        # Calculate ideal buying power based on desired allocation
        ideal_buying_power_needed = self.portfolio.cash * LEVERAGE_MULTIPLIER * self.account_allocation_per_trade

        
        self.log(
            f"calculate_order_quantity:{symbol}: available_buying_power: {available_buying_power}, ideal_buying_power_needed: {ideal_buying_power_needed}, Portfolio.Cash: {self.portfolio.Cash}, account_allocation_per_trade: {self.account_allocation_per_trade}"
        )

        # Use the minimum of ideal and available buying power
        usable_buying_power = min(available_buying_power, ideal_buying_power_needed)

        # Calculate quantity and round down to an integer
        quantity = int(usable_buying_power / price)

        # **Prefer buying at least 1 stock:**
        if quantity == 0 and usable_buying_power >= price:
            quantity = 1
            self.log(f"calculate_order_quantity: {symbol}: Buying at least 1 stock, even though ideal buying power was less than price.")
        elif quantity == 0:
            self.log(f"calculate_order_quantity: {symbol}: Cannot buy at least 1 stock, not enough buying power.")
            return 0
        self.log(
            f"calculate_order_quantity: {symbol}: Usable Buying Power: {usable_buying_power}, Quantity: {quantity}, price: {price}"
        )
        return quantity

    def get_long_order_quantity(self, symbol, price):
        """
        Gets the order quantity for a long position.

        Args:
            symbol: The symbol of the stock.
            price: The current price of the stock.

        Returns:
            The order quantity for a long position.
        """
        return self.calculate_order_quantity(symbol, price, OrderDirection.BUY)

    def get_short_order_quantity(self, symbol, price):
        """
        Gets the order quantity for a short position.

        Args:
            symbol: The symbol of the stock.
            price: The current price of the stock.

        Returns:
            The order quantity for a short position (negative).
        """
        quantity = self.calculate_order_quantity(symbol, price, OrderDirection.SELL)
        return quantity if quantity > 0 else 0  # Return negative quantity for short

    def is_index_security(self, ticker):
        if ticker in INDEX_TICKER_LIST:
            return True
        return False
    
    def is_market_currently_open(self):
        ''' Check if market is currently open. Mostly for test purposes'''

        self.add_equity('SPY', resolution=Resolution.Minute, extended_market_hours=False)

        self.log(f"INFO is_market_currently_open:: self time: {self.time}")

        is_open_now = self.securities["SPY"].exchange.hours.is_open(self.time, extended_market_hours=False)

        # check if current time is before next market close and after previous market open
        if is_open_now:
            self.log(f"INFO is_market_currently_open: Market is open!")
            self.remove_symbol_from_universe(self.get_us_equity_symbol_for_ticker('SPY'))
            return True 
        else:
            self.remove_symbol_from_universe(self.get_us_equity_symbol_for_ticker('SPY'))
            return False


    def ensure_long_position(self, symbol, close):

        self.log(f"INFO: ensure_long_position: long entry: {symbol}")

        if self.portfolio[symbol].is_long:
            return 

        if self.portfolio[symbol].is_short:
            self.liquidate(symbol)  # Liquidate short position
            self.log(f"INFO: ensure_long_position: liquidating short position for {symbol} for new buy entry")
            email(f"INFO: ensure_long_position: liquidating short position for {symbol} for new buy entry")
        
        quantity = self.get_long_order_quantity(symbol, close)

        self.stock_data[symbol.value].add_order_ticket(self.market_order(symbol, quantity))

        self.log(f"INFO: ensure_long_position: Buy {quantity} {symbol}")
        email(f"INFO: ensure_long_position: Buy {quantity} {symbol}")

        # Set profit target and stop loss
        self.set_profit_target_and_stop_loss(symbol, close, quantity, long=True)

    
    def ensure_short_position(self, symbol, close):

        self.log(f"INFO: ensure_short_position: Short entry: {symbol}, close: {close}")

        # if a position is already on
        if self.portfolio[symbol].is_long:
            self.liquidate(symbol)  # Liquidate long position
            self.log(f"INFO: ensure_short_position: liquidating long position for {symbol} for new short entry")
            email(f"INFO: ensure_short_position: liquidating long position for {symbol} for new short entry")

        quantity = self.get_short_order_quantity(symbol, close)

        self.stock_data[symbol.value].position_on = True
        self.stock_data[symbol.value].add_order_ticket(self.market_order(symbol, -quantity))

        self.log(f"INFO: ensure_short_position: Short {quantity} {symbol}")
        email(f"INFO: ensure_short_position: Short {quantity} {symbol}")

        # Set profit target and stop loss for short position
        self.set_profit_target_and_stop_loss(symbol, close, quantity, long=False)
    
    
    def set_profit_target_and_stop_loss(self, symbol, entry_price, quantity, long=True):
        '''Set profit target and stop loss for the given symbol'''

        # self.limit_order(symbol, -quantity if long else quantity, profit_target_price)
        # Sell 1 share of SPY through a trailing stop order that starts 5% above the current price

        if self.portfolio[symbol].is_long:
            self.trailing_stop_order(symbol.value, -quantity, trailing_amount = LONG_TRAILING_STOP_PCT, trailing_as_percentage = True)

        elif self.portfolio[symbol].is_short:
            self.trailing_stop_order(symbol.value, quantity, trailing_amount = SHORT_TRAILING_STOP_PCT, trailing_as_percentage = True)


    def on_brokerage_disconnect(self) -> None:
        self.log("Brokerage connection lost")
        email("Lean: Brokerage Connection Lost")

    def on_brokerage_message(self, message_event: BrokerageMessageEvent) -> None:
        self.log(f"Brokerage message received: {message_event.message}")

        email(f"Brokerage message received: {message_event.message}")

    def on_brokerage_disconnect(self) -> None:
        self.log("Brokerage connection lost")
        email("Lean: Brokerage Connection Lost")
        