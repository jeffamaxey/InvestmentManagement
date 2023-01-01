from datetime import datetime
import smart_value


def gen_val_xlsx(ticker):
    """generate or update a valuation file with argument, ticker"""

    smart_value.tools.stock_model.new_stock_model(ticker)


def update_pipeline_monitor():
    """Update the pipeline monitor"""

    o = smart_value.tools.monitor.Pipeline()
    o.load_opportunities()


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


if __name__ == '__main__':
    stare_list = ['0806.HK']
    for s in stare_list:
        gen_val_xlsx(s)
    # update_pipeline_monitor()
