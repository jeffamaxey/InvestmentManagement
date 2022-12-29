from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

url = "https://yh-finance.p.rapidapi.com/stock/v2/get-balance-sheet"

querystring = {"symbol": "1475.HK", "region": "US"}

headers = {
    "X-RapidAPI-Key": "33b113bc2amsha6696b232ae13c5p121434jsnd2600d0bcf71",
    "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
financials = json.loads(response.text)

revenues = []
cogs = []
op_expenses = []

print(financials['incomeStatementHistory']['incomeStatementHistory'])

for financial in financials['incomeStatementHistory']['incomeStatementHistory']:
    revenues.append(financial['totalRevenue']['raw'])
    cogs.append(financial['costOfRevenue']['raw'])
    op_expenses.append(financial['totalOperatingExpenses']['raw'])

print(revenues)
print(cogs)
print(op_expenses)