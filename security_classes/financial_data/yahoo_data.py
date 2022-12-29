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
        # YH Finance API, only called when necessary
        self.financials = None
        self.income_statement = None
        self.balance_sheet = None

    def retrieve_stock_info(self):
        """Returns a dictionary with stock information from yfinance package"""

        return Ticker(self.ticker).info

    def retrieve_financials(self):
        """Initialize the financial statement attributes a dictionary with financial data from YH Finance API"""

        # more info on YH finance API @ https://rapidapi.com/apidojo/api/yh-finance

        url = "https://yh-finance.p.rapidapi.com/stock/v2/get-balance-sheet"
        headers = {
            "X-RapidAPI-Key": "33b113bc2amsha6696b232ae13c5p121434jsnd2600d0bcf71",
            "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
        }
        querystring = {"symbol": self.ticker, "region": "US"}

        response = requests.request("GET", url, headers=headers, params=querystring)
        self.financials = json.loads(response.text)
        self.income_statement = self.get_income_statement()
        self.balance_sheet = self.get_balance_sheet()

    def get_income_statement(self):
        """Returns a DataFrame with selected income statement data"""
        sales = []
        cogs = []
        op_expenses = []
        interests = []
        net_income = []
        is_df = pd.DataFrame()

        for financial in self.financials['incomeStatementHistory']['incomeStatementHistory']:
            sales.append(financial['totalRevenue']['raw'])
            cogs.append(financial['costOfRevenue']['raw'])
            op_expenses.append(financial['sellingGeneralAdministrative']['raw'])
            interests.append(financial['interestExpense']['raw'])
            net_income.append(financial['netIncomeApplicableToCommonShares']['raw'])

        is_df['sales'] = sales
        is_df['cogs'] = cogs
        is_df['op_expense'] = op_expenses
        is_df['interests'] = interests
        is_df['net_income'] = net_income

        return is_df

    def get_balance_sheet(self):
        """Returns a DataFrame with selected balance sheet data"""

        total_assets = []
        current_assets = []
        current_liabilities = []
        short_debt = []
        long_debt = []
        equity = []
        minority_interest = []
        cash = []
        ppe = []
        bs_df = pd.DataFrame()

        last_year = self.financials['balanceSheetHistory']['balanceSheetStatements'][0]['endDate']

        for financial in self.financials['balanceSheetHistory']['balanceSheetStatements']:
            total_assets.append(financial['totalAssets']['raw'])
            current_assets.append(financial['totalCurrentAssets']['raw'])
            current_liabilities.append(financial['totalCurrentLiabilities']['raw'])
            short_debt.append(financial['sellingGeneralAdministrative']['raw'])
            long_debt.append(financial['interestExpense']['raw'])
            equity.append(financial['netIncomeApplicableToCommonShares']['raw'])
            minority_interest.append(financial['minorityInterest']['raw'])
            cash.append(financial['cash']['raw'])
            ppe.append(financial['propertyPlantEquipment']['raw'])

        bs_df['current_assets'] = current_assets
        bs_df['current_liabilities'] = current_liabilities
        bs_df['short_debt'] = short_debt
        bs_df['long_debt'] = long_debt
        bs_df['equity'] = equity
        bs_df['minority_interest'] = minority_interest
        bs_df['cash'] = cash
        bs_df['ppe'] = ppe

        return bs_df

    def csv_statements(self):
        """Export the income statement and balance sheet in csv format"""

        self.income_statement.to_csv(f'{self.ticker}_income_statement.csv', sep=',', encoding='utf-8')
        self.balance_sheet.to_csv(f'{self.ticker}_balance_sheet.csv', sep=',', encoding='utf-8')
