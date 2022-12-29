import requests
import pandas as pd
import json
from yfinance import Ticker
from datetime import datetime


class Financials:
    """Retrieves the data from YH Finance API and yfinance package"""
    def __init__(self, ticker):
        self.ticker = ticker
        # yfinance
        self.stock_info = self.retrieve_stock_info()
        self.name = self.stock_info['shortName']
        self.price = [self.stock_info['currentPrice'], self.stock_info['currency']]
        self.exchange = self.stock_info['exchange']
        self.shares = self.stock_info['sharesOutstanding']
        self.report_currency = self.stock_info['financialCurrency']
        self.next_earnings = pd.to_datetime(datetime.fromtimestamp(self.stock_info['mostRecentQuarter'])
                                            .strftime("%Y-%m-%d")) + pd.DateOffset(months=6)
        # YH Finance API
        self.financials = self.retrieve_financials()
        self.income_statement = self.financials
        self.balance_sheet = self.financials

    def retrieve_stock_info(self):
        """Returns a dictionary with stock information from yfinance package"""

        return Ticker(self.ticker).info

    def retrieve_financials(self):
        """Returns a dictionary with financial data from YH Finance API"""

        # more info on YH finance API @ https://rapidapi.com/apidojo/api/yh-finance

        url = "https://yh-finance.p.rapidapi.com/stock/v2/get-balance-sheet"
        headers = {
            "X-RapidAPI-Key": "33b113bc2amsha6696b232ae13c5p121434jsnd2600d0bcf71",
            "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
        }
        querystring = {"symbol": self.ticker, "region": "US"}

        response = requests.request("GET", url, headers=headers, params=querystring)
        return json.loads(response.text)

    def get_income_statement(self):
        """Returns a DataFrame with income statement data"""
        revenues = []
        cogs = []
        op_expenses = []

        for financial in self.financials['incomeStatementHistory']['incomeStatementHistory']:
            revenues.append(financial['totalRevenue']['raw'])
            cogs.append(financial['costOfRevenue']['raw'])
            op_expenses.append(financial['totalOperatingExpenses']['raw'])

        print(revenues)
        print(cogs)
        print(op_expenses)
        return None

    def get_balance_sheet(self):
        return None
