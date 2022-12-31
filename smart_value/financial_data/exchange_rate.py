from forex_python.converter import CurrencyRates


def get_forex_rate(buy, sell):
    """get exchange rate, buy means ask and sell means bid"""

    if buy != sell:
        c = CurrencyRates()
        return c.get_rate(buy, sell)
    else:
        return 1
