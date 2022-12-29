from securities import *
from financial_data import yahoo_data as yh
from financial_data import exchange_rate as fx

class Stock(Securities):
    """a type of Securities"""

    def __init__(self, security_code):
        """ """
        super().__init__(security_code)

        self.invest_horizon = 3  # 3 years holding period for stock by default
        self.report_currency = None
        self.is_df = None
        self.bs_df = None
        self.fx_rate = None

    def load_from_yf(self):
        """Scrap the financial_data from yfinance API"""

        ticker_data = yh.Financials(self.security_code)
        ticker_data.retrieve_financials()

        self.name = ticker_data.name
        self.price = ticker_data.price
        self.exchange = ticker_data.exchange
        self.shares = ticker_data.shares
        self.report_currency = ticker_data.report_currency
        self.fx_rate = fx.get_forex_rate(self.report_currency, self.price[1])
        self.next_earnings = ticker_data.next_earnings
        self.is_df = ticker_data.income_statement
        self.bs_df = ticker_data.balance_sheet
